#!/usr/bin/env python3
"""
Via Punctorum (Way of Points) Tracer

Traces active lines from the Judge backward through the Shield Chart
to identify the hidden protagonist figure at the root.

The Via Puncti technique reveals underlying causes:
- Fire line: intentions, desires, will
- Air line: thoughts, ideas, theories
- Water line: emotions, spiritual matters
- Earth line: material concerns, resources

Usage:
    python via_punctorum.py <shield_json_file>
    python via_punctorum.py --generate "Question"
    cat shield.json | python via_punctorum.py -
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ViaPath:
    """A traced path through the Shield Chart."""
    element: str  # 'fire', 'air', 'water', 'earth'
    path: list[str]  # Names of figures along the path
    root: str  # The hidden protagonist
    root_position: str  # Mother or Daughter position
    interpretation_hint: str


ELEMENT_MEANINGS = {
    'fire': {
        'name': 'Via Puncti Ignis',
        'meaning': 'intentions, desires, will, driving passion',
        'question': 'What do you truly WANT?',
    },
    'air': {
        'name': 'Via Puncti Aeris',
        'meaning': 'thoughts, ideas, theories, mental frameworks',
        'question': 'What are you THINKING?',
    },
    'water': {
        'name': 'Via Puncti Aquae',
        'meaning': 'emotions, feelings, spiritual undercurrents',
        'question': 'What do you FEEL?',
    },
    'earth': {
        'name': 'Via Puncti Terrae',
        'meaning': 'material concerns, resources, practical matters',
        'question': 'What RESOURCES are at stake?',
    },
}

POSITION_MEANINGS = {
    'Mother 1': 'The querent themselves - they are the root cause',
    'Mother 2': 'Resources and approach - material foundation is key',
    'Mother 3': 'Communication and environment - external forces',
    'Mother 4': 'Home, family, endings - the foundation matters',
    'Daughter 1': 'Creativity and pleasure - what they create',
    'Daughter 2': 'Work and health - daily circumstances',
    'Daughter 3': 'The other party - someone else is the driver',
    'Daughter 4': 'Transformation - death/rebirth energy at root',
}


def get_line(figure: dict, element: str) -> int:
    """Get the value of a specific elemental line from a figure."""
    return figure.get(element, figure['pattern'][
        {'fire': 0, 'air': 1, 'water': 2, 'earth': 3}[element]
    ])


def trace_via_puncti(chart: dict, element: str) -> Optional[ViaPath]:
    """
    Trace a Via Puncti path from Judge to root.

    Returns None if the element line is passive in the Judge.
    """
    judge = chart['judge']

    # Check if element is active in Judge
    if get_line(judge, element) == 0:
        return None  # Path doesn't exist for passive lines

    path = [judge['name']]

    # Trace through Witnesses
    rw = chart['right_witness']
    lw = chart['left_witness']

    rw_active = get_line(rw, element) == 1
    lw_active = get_line(lw, element) == 1

    if rw_active and not lw_active:
        # Path goes through Right Witness
        current_witness = rw
        witness_side = 'right'
        path.append(f"Right Witness: {rw['name']}")
    elif lw_active and not rw_active:
        # Path goes through Left Witness
        current_witness = lw
        witness_side = 'left'
        path.append(f"Left Witness: {lw['name']}")
    else:
        # Both active or both passive - path branches or doesn't exist cleanly
        # In traditional practice, this means multiple or no clear root
        return ViaPath(
            element=element,
            path=path + ["PATH BRANCHES - multiple roots"],
            root="Multiple/None",
            root_position="Ambiguous",
            interpretation_hint="The path branches, suggesting multiple influences or no single root cause.",
        )

    # Trace through Nieces
    nieces = chart['nieces']
    if witness_side == 'right':
        # Right side: Nieces 0 and 1
        n1_active = get_line(nieces[0], element) == 1
        n2_active = get_line(nieces[1], element) == 1
        if n1_active and not n2_active:
            current_niece = nieces[0]
            niece_idx = 0
            path.append(f"Niece 1: {nieces[0]['name']}")
        elif n2_active and not n1_active:
            current_niece = nieces[1]
            niece_idx = 1
            path.append(f"Niece 2: {nieces[1]['name']}")
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Nieces"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Niece level.",
            )
    else:
        # Left side: Nieces 2 and 3
        n3_active = get_line(nieces[2], element) == 1
        n4_active = get_line(nieces[3], element) == 1
        if n3_active and not n4_active:
            current_niece = nieces[2]
            niece_idx = 2
            path.append(f"Niece 3: {nieces[2]['name']}")
        elif n4_active and not n3_active:
            current_niece = nieces[3]
            niece_idx = 3
            path.append(f"Niece 4: {nieces[3]['name']}")
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Nieces"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Niece level.",
            )

    # Trace to root (Mother or Daughter)
    mothers = chart['mothers']
    daughters = chart['daughters']

    # Niece formation:
    # N1 = M1 + M2, N2 = M3 + M4
    # N3 = D1 + D2, N4 = D3 + D4
    if niece_idx == 0:
        # Niece 1 from M1 + M2
        m1_active = get_line(mothers[0], element) == 1
        m2_active = get_line(mothers[1], element) == 1
        if m1_active and not m2_active:
            root = mothers[0]
            position = 'Mother 1'
        elif m2_active and not m1_active:
            root = mothers[1]
            position = 'Mother 2'
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Mothers"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Mother level.",
            )
    elif niece_idx == 1:
        # Niece 2 from M3 + M4
        m3_active = get_line(mothers[2], element) == 1
        m4_active = get_line(mothers[3], element) == 1
        if m3_active and not m4_active:
            root = mothers[2]
            position = 'Mother 3'
        elif m4_active and not m3_active:
            root = mothers[3]
            position = 'Mother 4'
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Mothers"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Mother level.",
            )
    elif niece_idx == 2:
        # Niece 3 from D1 + D2
        d1_active = get_line(daughters[0], element) == 1
        d2_active = get_line(daughters[1], element) == 1
        if d1_active and not d2_active:
            root = daughters[0]
            position = 'Daughter 1'
        elif d2_active and not d1_active:
            root = daughters[1]
            position = 'Daughter 2'
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Daughters"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Daughter level.",
            )
    else:
        # Niece 4 from D3 + D4
        d3_active = get_line(daughters[2], element) == 1
        d4_active = get_line(daughters[3], element) == 1
        if d3_active and not d4_active:
            root = daughters[2]
            position = 'Daughter 3'
        elif d4_active and not d3_active:
            root = daughters[3]
            position = 'Daughter 4'
        else:
            return ViaPath(
                element=element,
                path=path + ["PATH BRANCHES at Daughters"],
                root="Multiple/None",
                root_position="Ambiguous",
                interpretation_hint="The path branches at the Daughter level.",
            )

    path.append(f"ROOT → {position}: {root['name']}")

    return ViaPath(
        element=element,
        path=path,
        root=root['name'],
        root_position=position,
        interpretation_hint=POSITION_MEANINGS.get(position, ""),
    )


def analyze_all_via_puncti(chart: dict) -> dict:
    """Trace Via Puncti for all four elements."""
    results = {}
    for element in ['fire', 'air', 'water', 'earth']:
        via = trace_via_puncti(chart, element)
        if via:
            results[element] = {
                'name': ELEMENT_MEANINGS[element]['name'],
                'meaning': ELEMENT_MEANINGS[element]['meaning'],
                'question': ELEMENT_MEANINGS[element]['question'],
                'path': via.path,
                'root': via.root,
                'root_position': via.root_position,
                'interpretation_hint': via.interpretation_hint,
            }
        else:
            results[element] = {
                'name': ELEMENT_MEANINGS[element]['name'],
                'status': 'inactive',
                'meaning': f"No Via Puncti exists for {element} (Judge's {element} line is passive)",
            }
    return results


def format_output(analysis: dict, chart: dict) -> str:
    """Format the Via Puncti analysis as readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("VIA PUNCTORUM ANALYSIS")
    lines.append("The Way of the Points")
    lines.append("=" * 60)
    lines.append("")

    judge_name = chart['judge']['name']
    lines.append(f"Judge: {judge_name}")
    lines.append("")

    for element in ['fire', 'air', 'water', 'earth']:
        info = analysis[element]
        lines.append("-" * 40)
        lines.append(f"{info['name'].upper()}")
        lines.append(f"({info['meaning']})")
        lines.append("")

        if 'status' in info and info['status'] == 'inactive':
            lines.append("  ✗ Path does not exist (passive line in Judge)")
        elif 'path' in info:
            lines.append("  Path traced:")
            for step in info['path']:
                lines.append(f"    → {step}")
            lines.append("")
            lines.append(f"  Hidden Protagonist: {info['root']}")
            lines.append(f"  Position: {info['root_position']}")
            if info['interpretation_hint']:
                lines.append(f"  Hint: {info['interpretation_hint']}")
        lines.append("")

    lines.append("=" * 60)

    # Traditional focus is Fire line
    if 'path' in analysis['fire'] and analysis['fire']['root'] != 'Multiple/None':
        lines.append("")
        lines.append("TRADITIONAL INTERPRETATION (Fire Line):")
        lines.append(f"The root intention/desire behind this question")
        lines.append(f"is found in {analysis['fire']['root_position']}: {analysis['fire']['root']}")
        lines.append("")
        lines.append(f"The figure {analysis['fire']['root']} reveals the driving")
        lines.append("force behind the situation.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Trace Via Punctorum paths through a Shield Chart"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="JSON file with chart data (use - for stdin)"
    )
    parser.add_argument(
        "--generate",
        "-g",
        metavar="QUESTION",
        help="Generate a new chart with this question first"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--element",
        "-e",
        choices=['fire', 'air', 'water', 'earth'],
        help="Only trace specific element"
    )

    args = parser.parse_args()

    # Get or generate chart
    if args.generate:
        # Import and use generate_shield
        from generate_shield import generate_shield
        chart_obj = generate_shield(question=args.generate)
        chart = chart_obj.to_dict()
    else:
        # Read from file or stdin
        if args.input == "-":
            chart = json.load(sys.stdin)
        else:
            with open(args.input) as f:
                chart = json.load(f)

    # Analyze
    if args.element:
        via = trace_via_puncti(chart, args.element)
        if args.json:
            if via:
                print(json.dumps({
                    'element': via.element,
                    'path': via.path,
                    'root': via.root,
                    'root_position': via.root_position,
                    'interpretation_hint': via.interpretation_hint,
                }, indent=2))
            else:
                print(json.dumps({'element': args.element, 'status': 'inactive'}))
        else:
            if via:
                print(f"Via Puncti {args.element.title()}:")
                for step in via.path:
                    print(f"  → {step}")
                print(f"\nRoot: {via.root} ({via.root_position})")
            else:
                print(f"No Via Puncti for {args.element} (passive in Judge)")
    else:
        analysis = analyze_all_via_puncti(chart)
        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print(format_output(analysis, chart))


if __name__ == "__main__":
    main()
