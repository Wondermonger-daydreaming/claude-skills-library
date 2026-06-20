#!/usr/bin/env python3
"""
Geomantic Shield Chart Generator

Generates complete Shield Charts from random or seeded input,
deriving all 16 figures through proper geomantic mathematics.

Usage:
    python generate_shield.py                     # Random generation
    python generate_shield.py "My question"       # Seeded from question
    python generate_shield.py --seed 12345        # Explicit seed
    python generate_shield.py --json              # JSON output
"""

import argparse
import hashlib
import json
import random
import sys
import time
from dataclasses import dataclass
from typing import Optional

# The sixteen geomantic figures.
# Each figure is four element-lines read TOP -> BOTTOM as (Fire, Air, Water, Earth).
# There are exactly 2**4 = 16 figures, one per distinct pattern. Any table with a
# repeated or missing pattern is corrupt; _self_test() (below) enforces this so the
# old collision bug (Conjunctio/Carcer/Acquisitio sharing a pattern, Caput/Cauda and
# Fortuna Major/Minor swapped) can never silently return. Patterns triangulated from
# three independent source-surveys staged in _staging/geomancy-{antiquary,cartographer,
# inquisitor}.md (Agrippa/Cattan/Fludd; Greer/Wikipedia; Skinner/Golden Dawn), reconciled
# against reversion symmetry and the four single-active "pure element" figures.
#
# FORMALISM: geomantic addition is bitwise XOR, so the 16 figures form the elementary
# abelian 2-group (Z/2)^4 (Robert Jaulin, *La Geomancie: analyse formelle*, 1966) -- with
# Populus the identity and every figure its own inverse. _self_test() asserts this; the
# Arabic root (ilm al-raml) and the full formal account are in references/PROVENANCE.md.
#
# NOTE on contested fields: dot-PATTERNS are invariant across the whole tradition and are
# load-bearing (they identify the figure). PLANET attributions are the standard diurnal/
# nocturnal pairing (also convergent). ELEMENT and zodiac genuinely DIVERGE between
# traditions (inner/geometric vs. "vulgar"; planetary-rulership vs. Golden-Dawn zodiac) --
# the element values here are one defensible choice; see the staged files for the variants.

# Encoding for this block of tables: 1 = single point (active), 2 = double point (passive).
FIGURES = {
    (1, 1, 1, 1): 'Via',                # ● ● ● ●
    (2, 2, 2, 2): 'Populus',            # ●● ●● ●● ●●
    (2, 1, 1, 2): 'Conjunctio',         # ●● ● ● ●●
    (1, 2, 2, 1): 'Carcer',             # ● ●● ●● ●
    (2, 1, 1, 1): 'Caput Draconis',     # ●● ● ● ●
    (1, 1, 1, 2): 'Cauda Draconis',     # ● ● ● ●●
    (2, 2, 1, 1): 'Fortuna Major',      # ●● ●● ● ●
    (1, 1, 2, 2): 'Fortuna Minor',      # ● ● ●● ●●
    (2, 1, 2, 1): 'Acquisitio',         # ●● ● ●● ●
    (1, 2, 1, 2): 'Amissio',            # ● ●● ● ●●
    (1, 2, 2, 2): 'Laetitia',           # ● ●● ●● ●●
    (2, 2, 2, 1): 'Tristitia',          # ●● ●● ●● ●
    (1, 1, 2, 1): 'Puer',               # ● ● ●● ●
    (1, 2, 1, 1): 'Puella',             # ● ●● ● ●
    (2, 1, 2, 2): 'Rubeus',             # ●● ● ●● ●●
    (2, 2, 1, 2): 'Albus',              # ●● ●● ● ●●
}

FIGURE_PATTERNS = {
    'Via'             : (1, 1, 1, 1),
    'Populus'         : (2, 2, 2, 2),
    'Conjunctio'      : (2, 1, 1, 2),
    'Carcer'          : (1, 2, 2, 1),
    'Caput Draconis'  : (2, 1, 1, 1),
    'Cauda Draconis'  : (1, 1, 1, 2),
    'Fortuna Major'   : (2, 2, 1, 1),
    'Fortuna Minor'   : (1, 1, 2, 2),
    'Acquisitio'      : (2, 1, 2, 1),
    'Amissio'         : (1, 2, 1, 2),
    'Laetitia'        : (1, 2, 2, 2),
    'Tristitia'       : (2, 2, 2, 1),
    'Puer'            : (1, 1, 2, 1),
    'Puella'          : (1, 2, 1, 1),
    'Rubeus'          : (2, 1, 2, 2),
    'Albus'           : (2, 2, 1, 2),
}

# Reverse lookup: pattern -> name. Patterns are unique, so this is a clean bijection
# (the historical Conjunctio/Carcer dedup hack is no longer needed and was removed).
PATTERN_TO_NAME = {v: k for k, v in FIGURE_PATTERNS.items()}

# Standard planetary attributions (diurnal/nocturnal pairs) + a defensible element.
FIGURE_DATA = {
    'Via'             : {"pattern": (1, 1, 1, 1), "planet": 'Moon', "element": 'Water'},
    'Populus'         : {"pattern": (2, 2, 2, 2), "planet": 'Moon', "element": 'Water'},
    'Conjunctio'      : {"pattern": (2, 1, 1, 2), "planet": 'Mercury', "element": 'Air'},
    'Carcer'          : {"pattern": (1, 2, 2, 1), "planet": 'Saturn', "element": 'Earth'},
    'Caput Draconis'  : {"pattern": (2, 1, 1, 1), "planet": 'North Node', "element": 'Earth'},
    'Cauda Draconis'  : {"pattern": (1, 1, 1, 2), "planet": 'South Node', "element": 'Fire'},
    'Fortuna Major'   : {"pattern": (2, 2, 1, 1), "planet": 'Sun', "element": 'Fire'},
    'Fortuna Minor'   : {"pattern": (1, 1, 2, 2), "planet": 'Sun', "element": 'Fire'},
    'Acquisitio'      : {"pattern": (2, 1, 2, 1), "planet": 'Jupiter', "element": 'Air'},
    'Amissio'         : {"pattern": (1, 2, 1, 2), "planet": 'Venus', "element": 'Earth'},
    'Laetitia'        : {"pattern": (1, 2, 2, 2), "planet": 'Jupiter', "element": 'Water'},
    'Tristitia'       : {"pattern": (2, 2, 2, 1), "planet": 'Saturn', "element": 'Earth'},
    'Puer'            : {"pattern": (1, 1, 2, 1), "planet": 'Mars', "element": 'Fire'},
    'Puella'          : {"pattern": (1, 2, 1, 1), "planet": 'Venus', "element": 'Air'},
    'Rubeus'          : {"pattern": (2, 1, 2, 2), "planet": 'Mars', "element": 'Fire'},
    'Albus'           : {"pattern": (2, 2, 1, 2), "planet": 'Mercury', "element": 'Water'},
}

# CORRECTED binary form. Encoding: (Fire, Air, Water, Earth) where 1 = active (single, ●),
# 0 = passive (double, ●●).
FIGURES_BINARY = {
    'Via'             : (1, 1, 1, 1),
    'Populus'         : (0, 0, 0, 0),
    'Conjunctio'      : (0, 1, 1, 0),
    'Carcer'          : (1, 0, 0, 1),
    'Caput Draconis'  : (0, 1, 1, 1),
    'Cauda Draconis'  : (1, 1, 1, 0),
    'Fortuna Major'   : (0, 0, 1, 1),
    'Fortuna Minor'   : (1, 1, 0, 0),
    'Acquisitio'      : (0, 1, 0, 1),
    'Amissio'         : (1, 0, 1, 0),
    'Laetitia'        : (1, 0, 0, 0),
    'Tristitia'       : (0, 0, 0, 1),
    'Puer'            : (1, 1, 0, 1),
    'Puella'          : (1, 0, 1, 1),
    'Rubeus'          : (0, 1, 0, 0),
    'Albus'           : (0, 0, 1, 0),
}

# Same 16 figures as an ordered list of (name, fire, air, water, earth); 1=single/active, 0=double/passive.
GEOMANTIC_FIGURES = [
    ('Via', 1, 1, 1, 1),                      # ● ● ● ●
    ('Populus', 0, 0, 0, 0),                  # ●● ●● ●● ●●
    ('Conjunctio', 0, 1, 1, 0),               # ●● ● ● ●●
    ('Carcer', 1, 0, 0, 1),                   # ● ●● ●● ●
    ('Caput Draconis', 0, 1, 1, 1),           # ●● ● ● ●
    ('Cauda Draconis', 1, 1, 1, 0),           # ● ● ● ●●
    ('Fortuna Major', 0, 0, 1, 1),            # ●● ●● ● ●
    ('Fortuna Minor', 1, 1, 0, 0),            # ● ● ●● ●●
    ('Acquisitio', 0, 1, 0, 1),               # ●● ● ●● ●
    ('Amissio', 1, 0, 1, 0),                  # ● ●● ● ●●
    ('Laetitia', 1, 0, 0, 0),                 # ● ●● ●● ●●
    ('Tristitia', 0, 0, 0, 1),                # ●● ●● ●● ●
    ('Puer', 1, 1, 0, 1),                     # ● ● ●● ●
    ('Puella', 1, 0, 1, 1),                   # ● ●● ● ●
    ('Rubeus', 0, 1, 0, 0),                   # ●● ● ●● ●●
    ('Albus', 0, 0, 1, 0),                    # ●● ●● ● ●●
]

# Build lookup from pattern (active=1/passive=0) to figure name -- used at runtime by Figure.
PATTERN_LOOKUP = {
    (1, 1, 1, 1): 'Via',
    (0, 0, 0, 0): 'Populus',
    (0, 1, 1, 0): 'Conjunctio',
    (1, 0, 0, 1): 'Carcer',
    (0, 1, 1, 1): 'Caput Draconis',
    (1, 1, 1, 0): 'Cauda Draconis',
    (0, 0, 1, 1): 'Fortuna Major',
    (1, 1, 0, 0): 'Fortuna Minor',
    (0, 1, 0, 1): 'Acquisitio',
    (1, 0, 1, 0): 'Amissio',
    (1, 0, 0, 0): 'Laetitia',
    (0, 0, 0, 1): 'Tristitia',
    (1, 1, 0, 1): 'Puer',
    (1, 0, 1, 1): 'Puella',
    (0, 1, 0, 0): 'Rubeus',
    (0, 0, 1, 0): 'Albus',
}


def _self_test() -> None:
    """Guard against a corrupted figure table (the bug this file used to ship)."""
    from itertools import product
    full = set(product((0, 1), repeat=4))
    assert len(PATTERN_LOOKUP) == 16 and set(PATTERN_LOOKUP) == full, "PATTERN_LOOKUP not the full unique 2**4"
    assert len(FIGURES_BINARY) == 16 and set(FIGURES_BINARY.values()) == full, "FIGURES_BINARY not unique/full"
    assert len(set(FIGURE_PATTERNS.values())) == 16, "FIGURE_PATTERNS has duplicates"
    # the 1/2-encoded tables and the 0/1-encoded tables must describe the same figures
    for name, bits in FIGURES_BINARY.items():
        twelve = tuple(1 if b else 2 for b in bits)
        assert FIGURE_PATTERNS[name] == twelve, f"encoding mismatch for {name}"
        assert PATTERN_LOOKUP[bits] == name, f"PATTERN_LOOKUP mismatch for {name}"
        assert FIGURE_DATA[name]["pattern"] == twelve, f"FIGURE_DATA pattern mismatch for {name}"
    # reversion (upside-down) pairs must hold
    refl = lambda p: (p[3], p[2], p[1], p[0])
    for a, b in [("Puer", "Puella"), ("Albus", "Rubeus"), ("Caput Draconis", "Cauda Draconis"),
                 ("Laetitia", "Tristitia"), ("Acquisitio", "Amissio"), ("Fortuna Major", "Fortuna Minor")]:
        assert refl(FIGURES_BINARY[a]) == FIGURES_BINARY[b], f"reversion {a}/{b}"
    # GROUP STRUCTURE: geomantic addition is bitwise XOR, so the 16 figures form the
    # elementary abelian 2-group (Z/2)^4 (Jaulin 1966; see references/PROVENANCE.md).
    # Populus is the identity; every figure is its own inverse; the set is closed.
    xor = lambda p, q: tuple((a + b) % 2 for a, b in zip(p, q))
    pops = FIGURES_BINARY["Populus"]
    assert pops == (0, 0, 0, 0), "Populus must be the all-passive identity 0000"
    for p in FIGURES_BINARY.values():
        assert xor(p, pops) == p, "Populus must be the additive identity (x XOR 0 = x)"
        assert xor(p, p) == pops, "every figure must be its own inverse (x XOR x = Populus)"
    allp = set(FIGURES_BINARY.values())
    assert all(xor(p, q) in allp for p in allp for q in allp), "(Z/2)^4 not closed under addition"


_self_test()


@dataclass
class Figure:
    """A geomantic figure with its four elemental lines."""
    fire: int    # 1 = active (●), 0 = passive (●●)
    air: int
    water: int
    earth: int
    name: str = ""

    def __post_init__(self):
        if not self.name:
            pattern = (self.fire, self.air, self.water, self.earth)
            self.name = PATTERN_LOOKUP.get(pattern, "Unknown")

    @property
    def pattern(self) -> tuple:
        return (self.fire, self.air, self.water, self.earth)

    def __str__(self) -> str:
        return self.name

    def to_ascii(self) -> str:
        """Return ASCII representation of the figure."""
        lines = []
        for val in [self.fire, self.air, self.water, self.earth]:
            if val == 1:
                lines.append("  ●  ")
            else:
                lines.append(" ● ● ")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pattern": list(self.pattern),
            "fire": self.fire,
            "air": self.air,
            "water": self.water,
            "earth": self.earth,
        }


def generate_random_line(rng: random.Random) -> int:
    """Generate a random line (0 or 1)."""
    return rng.randint(0, 1)


def generate_mother(rng: random.Random) -> Figure:
    """Generate a random Mother figure."""
    return Figure(
        fire=generate_random_line(rng),
        air=generate_random_line(rng),
        water=generate_random_line(rng),
        earth=generate_random_line(rng),
    )


def add_figures(fig1: Figure, fig2: Figure) -> Figure:
    """Add two figures using geomantic addition: per-line XOR (the group law of (Z/2)^4).

    'Lines different -> single/active; lines same -> double/passive' = addition mod 2.
    See references/PROVENANCE.md (Jaulin 1966).
    """
    return Figure(
        fire=(fig1.fire + fig2.fire) % 2,
        air=(fig1.air + fig2.air) % 2,
        water=(fig1.water + fig2.water) % 2,
        earth=(fig1.earth + fig2.earth) % 2,
    )


def transpose_mothers(mothers: list[Figure]) -> list[Figure]:
    """Derive the four Daughters by transposing the Mothers."""
    daughters = []
    # D1: Fire lines of M1,M2,M3,M4 become F,A,W,E of D1
    # D2: Air lines of M1,M2,M3,M4 become F,A,W,E of D2
    # etc.
    for attr in ['fire', 'air', 'water', 'earth']:
        daughter = Figure(
            fire=getattr(mothers[0], attr),
            air=getattr(mothers[1], attr),
            water=getattr(mothers[2], attr),
            earth=getattr(mothers[3], attr),
        )
        daughters.append(daughter)
    return daughters


@dataclass
class ShieldChart:
    """Complete Shield Chart with all 16 (or 17) figures."""
    mothers: list[Figure]
    daughters: list[Figure]
    nieces: list[Figure]
    right_witness: Figure
    left_witness: Figure
    judge: Figure
    sentence: Optional[Figure] = None
    question: str = ""
    seed: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "seed": self.seed,
            "mothers": [m.to_dict() for m in self.mothers],
            "daughters": [d.to_dict() for d in self.daughters],
            "nieces": [n.to_dict() for n in self.nieces],
            "right_witness": self.right_witness.to_dict(),
            "left_witness": self.left_witness.to_dict(),
            "judge": self.judge.to_dict(),
            "sentence": self.sentence.to_dict() if self.sentence else None,
        }

    def find_repetitions(self) -> dict[str, int]:
        """Find figures that appear more than once."""
        all_figures = (
            self.mothers + self.daughters + self.nieces +
            [self.right_witness, self.left_witness, self.judge]
        )
        if self.sentence:
            all_figures.append(self.sentence)

        counts = {}
        for fig in all_figures:
            counts[fig.name] = counts.get(fig.name, 0) + 1
        return {k: v for k, v in counts.items() if v > 1}

    def validate(self) -> bool:
        """Check the chart's structural integrity against the (Z/2)^4 group theorems.

        Three facts, all consequences of geomantic addition being bitwise XOR (Jaulin
        1966; verified empirically 4000/4000; see references/PROVENANCE.md), where the
        four Mothers are read as a 4x4 binary matrix (row i = Mother i, columns = Fire,
        Air, Water, Earth):
          - Right Witness == the column-parities of that matrix
          - Left  Witness == the row-parities
          - Judge == column-parity XOR row-parity, and so has EVEN total parity.
        A failure here means the derivation (transpose / addition) is broken.
        """
        def bits(f):
            return (f.fire, f.air, f.water, f.earth)
        par = lambda v: sum(v) % 2
        m = [bits(x) for x in self.mothers]
        col_par = tuple(par([m[i][j] for i in range(4)]) for j in range(4))
        row_par = tuple(par(m[j]) for j in range(4))
        judge_pred = tuple(col_par[k] ^ row_par[k] for k in range(4))
        return (
            bits(self.right_witness) == col_par
            and bits(self.left_witness) == row_par
            and bits(self.judge) == judge_pred
            and par(bits(self.judge)) == 0
        )

    def to_ascii(self) -> str:
        """Generate ASCII representation of the full Shield Chart."""
        lines = []
        lines.append("╔" + "═" * 76 + "╗")
        lines.append("║" + "SHIELD CHART".center(76) + "║")
        if self.question:
            q = self.question[:70]
            lines.append("║" + f"Question: {q}".center(76) + "║")
        lines.append("╠" + "═" * 76 + "╣")

        # Mothers and Daughters row
        def fig_col(fig: Figure, width: int = 9) -> list[str]:
            """Generate column for a figure."""
            rows = []
            for val in [fig.fire, fig.air, fig.water, fig.earth]:
                if val == 1:
                    rows.append("●".center(width))
                else:
                    rows.append("● ●".center(width))
            rows.append(fig.name[:width].center(width))
            return rows

        # Build mother/daughter row
        m_cols = [fig_col(m) for m in self.mothers]
        d_cols = [fig_col(d) for d in self.daughters]

        for i in range(5):  # 4 lines + name
            row = "║ "
            for col in m_cols:
                row += col[i] + " "
            row += "│ "
            for col in d_cols:
                row += col[i] + " "
            row = row.ljust(77) + "║"
            lines.append(row)

        lines.append("╠" + "═" * 76 + "╣")

        # Nieces row
        n_cols = [fig_col(n, 16) for n in self.nieces]
        for i in range(5):
            row = "║ "
            row += n_cols[0][i] + "  " + n_cols[1][i]
            row += " │ "
            row += n_cols[2][i] + "  " + n_cols[3][i]
            row = row.ljust(77) + "║"
            lines.append(row)

        lines.append("╠" + "═" * 76 + "╣")

        # Witnesses row
        rw_col = fig_col(self.right_witness, 20)
        lw_col = fig_col(self.left_witness, 20)
        for i in range(5):
            row = "║ "
            row += rw_col[i].center(35)
            row += " │ "
            row += lw_col[i].center(35)
            row = row.ljust(77) + "║"
            lines.append(row)

        lines.append("╠" + "═" * 76 + "╣")

        # Judge
        j_col = fig_col(self.judge, 20)
        for i in range(5):
            row = "║" + j_col[i].center(76) + "║"
            lines.append(row)

        # Sentence (if present)
        if self.sentence:
            lines.append("╠" + "═" * 76 + "╣")
            lines.append("║" + "SENTENCE".center(76) + "║")
            s_col = fig_col(self.sentence, 20)
            for i in range(5):
                row = "║" + s_col[i].center(76) + "║"
                lines.append(row)

        lines.append("╚" + "═" * 76 + "╝")

        return "\n".join(lines)


def generate_shield(
    question: Optional[str] = None,
    seed: Optional[int] = None,
    include_sentence: bool = True
) -> ShieldChart:
    """Generate a complete Shield Chart."""

    # Determine seed
    if seed is None:
        if question:
            # Hash question with timestamp for unique seed
            combined = question + str(time.time())
            hash_bytes = hashlib.sha256(combined.encode()).digest()
            seed = int.from_bytes(hash_bytes[:8], 'big')
        else:
            seed = int(time.time() * 1000000)

    rng = random.Random(seed)

    # Generate Mothers
    mothers = [generate_mother(rng) for _ in range(4)]

    # Derive Daughters
    daughters = transpose_mothers(mothers)

    # Calculate Nieces
    nieces = [
        add_figures(mothers[0], mothers[1]),   # N1
        add_figures(mothers[2], mothers[3]),   # N2
        add_figures(daughters[0], daughters[1]),  # N3
        add_figures(daughters[2], daughters[3]),  # N4
    ]

    # Calculate Witnesses
    right_witness = add_figures(nieces[0], nieces[1])
    left_witness = add_figures(nieces[2], nieces[3])

    # Calculate Judge
    judge = add_figures(right_witness, left_witness)

    # Calculate Sentence (optional)
    sentence = None
    if include_sentence:
        sentence = add_figures(judge, mothers[0])

    return ShieldChart(
        mothers=mothers,
        daughters=daughters,
        nieces=nieces,
        right_witness=right_witness,
        left_witness=left_witness,
        judge=judge,
        sentence=sentence,
        question=question or "",
        seed=seed,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate a geomantic Shield Chart"
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to seed the chart (optional)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Explicit random seed"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--no-sentence",
        action="store_true",
        help="Omit the Sentence/Reconciler"
    )

    args = parser.parse_args()

    chart = generate_shield(
        question=args.question,
        seed=args.seed,
        include_sentence=not args.no_sentence,
    )

    if args.json:
        print(json.dumps(chart.to_dict(), indent=2))
    else:
        print(chart.to_ascii())
        print()

        # Print repetitions
        reps = chart.find_repetitions()
        if reps:
            print("Repeated figures:")
            for name, count in reps.items():
                print(f"  {name}: {count}x")
        print()
        print(f"Seed: {chart.seed}")


if __name__ == "__main__":
    main()
