#!/usr/bin/env python3
"""
Yijing Session Management

Tracks a querent's journey across multiple readings, enabling pattern detection,
outcome tracking, and the accumulation of oracular wisdom over time.

The session system transforms ephemeral consultations into persistent relationships
with the Changes—each reading building on what came before.

Classes:
    ReadingRecord: A single hexagram reading with full context
    PatternAnalysis: Detected patterns across session readings
    ConsultationSession: The querent's journey through multiple readings
    SessionManager: Manages session lifecycle and persistence
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


def utc_now() -> str:
    """Return current UTC time as ISO format string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Import from sibling module (cast_hexagram.py)
try:
    from cast_hexagram import Hexagram, TRIGRAMS, HEXAGRAM_NAMES
except ImportError:
    # For standalone testing
    Hexagram = None
    TRIGRAMS = {}
    HEXAGRAM_NAMES = {}


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ReadingOutcome(Enum):
    """Querent-assessed outcome of a reading."""
    PENDING = "pending"           # Not yet assessed
    CONFIRMED = "confirmed"       # Reading proved accurate
    PARTIAL = "partial"           # Partially applicable
    UNCLEAR = "unclear"           # Still unclear
    CONTRADICTED = "contradicted" # Events went differently


class SessionStatus(Enum):
    """Status of a consultation session."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    CLOSED = "closed"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ReadingRecord:
    """
    A single hexagram reading with full context.
    Persists the ephemeral Hexagram object plus metadata for pattern analysis.
    """
    # Identity
    id: str                               # UUID for this reading
    timestamp: str                        # ISO format datetime

    # The question
    question: str

    # Hexagram data (from Hexagram.to_dict())
    primary_hexagram: int                 # King Wen number (1-64)
    primary_name: Dict[str, str]          # {chinese, pinyin, english}
    lines: List[Dict[str, Any]]           # All 6 line values and properties
    moving_lines: List[int]               # Positions of changing lines

    # Trigram analysis
    lower_trigram: Dict[str, str]         # {name, symbol, element, image}
    upper_trigram: Dict[str, str]

    # Derived hexagrams
    nuclear_hexagram: Optional[int] = None
    relating_hexagram: Optional[int] = None

    # Generation metadata
    method: str = "yarrow"
    seed: Optional[int] = None

    # Post-reading fields (updated later)
    outcome: str = "pending"              # ReadingOutcome value
    outcome_notes: str = ""
    outcome_timestamp: Optional[str] = None

    # Tags for pattern detection
    themes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReadingRecord':
        """Deserialize from JSON storage."""
        return cls(**data)

    @classmethod
    def from_hexagram(cls, hexagram: 'Hexagram', question: str) -> 'ReadingRecord':
        """
        Factory to create ReadingRecord from existing Hexagram object.

        Args:
            hexagram: The cast Hexagram object
            question: The querent's question

        Returns:
            A new ReadingRecord capturing the full context
        """
        hex_dict = hexagram.to_dict()

        return cls(
            id=str(uuid.uuid4()),
            timestamp=utc_now(),
            question=question,
            primary_hexagram=hex_dict["number"],
            primary_name=hex_dict["name"],
            lines=hex_dict["lines"],
            moving_lines=hex_dict["moving_lines"],
            lower_trigram=hex_dict["lower_trigram"],
            upper_trigram=hex_dict["upper_trigram"],
            nuclear_hexagram=hex_dict.get("nuclear_hexagram", {}).get("number"),
            relating_hexagram=hex_dict.get("relating_hexagram", {}).get("number"),
            method=hex_dict["method"],
            seed=hex_dict["seed"],
        )

    def record_outcome(
        self,
        outcome: str,
        notes: str = ""
    ) -> None:
        """
        Record the outcome of this reading.

        Args:
            outcome: One of ReadingOutcome values
            notes: Optional notes about the outcome
        """
        self.outcome = outcome
        self.outcome_notes = notes
        self.outcome_timestamp = utc_now()


@dataclass
class PatternAnalysis:
    """
    Detected patterns across a session's readings.

    Reveals what individual readings cannot: recurring energies, elemental
    imbalances, and transformation patterns in the querent's journey.
    """
    # Frequency counts
    trigram_frequencies: Dict[str, int]     # {trigram_name: count}
    element_frequencies: Dict[str, int]     # {element: count}
    hexagram_frequencies: Dict[int, int]    # {hex_number: count}

    # Recurring patterns (significant repetitions)
    recurring_trigrams: List[str]           # Trigrams appearing 3+ times
    recurring_hexagrams: List[int]          # Hexagrams appearing 2+ times

    # Element balance assessment
    element_balance: Dict[str, str]         # {element: "excess"|"deficient"|"balanced"}

    # Structural patterns
    moving_line_positions: Dict[int, int]   # Position frequency (1-6)
    transformation_pairs: List[Tuple[int, int]]  # [(primary, relating), ...]

    # Metadata
    reading_count: int = 0
    generated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for output."""
        return asdict(self)

    def get_insights(self) -> List[str]:
        """
        Generate human-readable insights from the patterns.

        Returns:
            List of insight strings
        """
        insights = []

        # Recurring trigrams
        if self.recurring_trigrams:
            trigram_str = ", ".join(self.recurring_trigrams)
            insights.append(
                f"Recurring trigrams: {trigram_str}. "
                "These energies repeatedly appear in your consultations."
            )

        # Element imbalances
        excess = [e for e, s in self.element_balance.items() if s == "excess"]
        deficient = [e for e, s in self.element_balance.items() if s == "deficient"]

        if excess:
            insights.append(
                f"Elemental excess: {', '.join(excess)}. "
                "Consider whether this energy dominates your situation."
            )
        if deficient:
            insights.append(
                f"Elemental deficiency: {', '.join(deficient)}. "
                "This energy may be lacking in your current circumstances."
            )

        # Moving line patterns
        active_positions = [
            pos for pos, count in self.moving_line_positions.items()
            if count >= 3
        ]
        if active_positions:
            pos_str = ", ".join(str(p) for p in active_positions)
            insights.append(
                f"Active line positions: {pos_str}. "
                "These positions frequently carry the message of change."
            )

        return insights


@dataclass
class ConsultationSession:
    """
    Tracks a querent's journey across multiple readings.

    The session is the central organizing unit—it holds the timeline of readings,
    enables pattern analysis, and persists across invocations.
    """
    # Identity
    id: str                                 # Short UUID for CLI friendliness
    name: str                               # Human-readable name
    created_at: str                         # ISO datetime
    last_accessed: str                      # ISO datetime

    # Identity (optional)
    querent_name: Optional[str] = None      # Optional name
    querent_notes: str = ""                 # Personal context

    # The readings timeline
    readings: List[ReadingRecord] = field(default_factory=list)

    # Session metadata
    status: str = "active"                  # active, archived, closed
    purpose: str = ""                       # Why session was started

    def add_reading(self, reading: ReadingRecord) -> None:
        """
        Add a reading to the session timeline.

        Args:
            reading: The ReadingRecord to add
        """
        self.readings.append(reading)
        self.last_accessed = utc_now()

    def get_reading(self, reading_id: str) -> Optional[ReadingRecord]:
        """
        Get a specific reading by ID.

        Args:
            reading_id: The reading's UUID

        Returns:
            The ReadingRecord or None if not found
        """
        for reading in self.readings:
            if reading.id == reading_id:
                return reading
        return None

    def get_patterns(self) -> PatternAnalysis:
        """
        Analyze patterns across all readings in this session.

        Returns:
            PatternAnalysis with detected patterns
        """
        if not self.readings:
            return PatternAnalysis(
                trigram_frequencies={},
                element_frequencies={},
                hexagram_frequencies={},
                recurring_trigrams=[],
                recurring_hexagrams=[],
                element_balance={},
                moving_line_positions={pos: 0 for pos in range(1, 7)},
                transformation_pairs=[],
                reading_count=0,
                generated_at=utc_now()
            )

        # Trigram frequency
        trigram_freq: Dict[str, int] = {}
        for reading in self.readings:
            for trig in [reading.lower_trigram, reading.upper_trigram]:
                name = trig.get("name", "Unknown")
                trigram_freq[name] = trigram_freq.get(name, 0) + 1

        # Element frequency (from trigrams)
        element_freq: Dict[str, int] = {}
        for reading in self.readings:
            for trig in [reading.lower_trigram, reading.upper_trigram]:
                elem = trig.get("element", "Unknown")
                element_freq[elem] = element_freq.get(elem, 0) + 1

        # Hexagram frequency (primary + nuclear + relating)
        hex_freq: Dict[int, int] = {}
        for reading in self.readings:
            for h in [
                reading.primary_hexagram,
                reading.nuclear_hexagram,
                reading.relating_hexagram
            ]:
                if h:
                    hex_freq[h] = hex_freq.get(h, 0) + 1

        # Moving line position frequency
        position_freq: Dict[int, int] = {i: 0 for i in range(1, 7)}
        for reading in self.readings:
            for pos in reading.moving_lines:
                position_freq[pos] += 1

        # Transformation pairs (primary -> relating)
        pairs: List[Tuple[int, int]] = []
        for reading in self.readings:
            if reading.relating_hexagram:
                pairs.append((reading.primary_hexagram, reading.relating_hexagram))

        # Calculate recurring patterns
        recurring_trig = [t for t, c in trigram_freq.items() if c >= 3]
        recurring_hex = [h for h, c in hex_freq.items() if c >= 2]

        # Element balance assessment
        total_elements = sum(element_freq.values())
        expected = total_elements / 5 if total_elements > 0 else 1
        element_balance: Dict[str, str] = {}
        for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
            count = element_freq.get(elem, 0)
            if count > expected * 1.5:
                element_balance[elem] = "excess"
            elif count < expected * 0.5:
                element_balance[elem] = "deficient"
            else:
                element_balance[elem] = "balanced"

        return PatternAnalysis(
            trigram_frequencies=trigram_freq,
            element_frequencies=element_freq,
            hexagram_frequencies=hex_freq,
            recurring_trigrams=recurring_trig,
            recurring_hexagrams=recurring_hex,
            element_balance=element_balance,
            moving_line_positions=position_freq,
            transformation_pairs=pairs,
            reading_count=len(self.readings),
            generated_at=utc_now()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "querent_name": self.querent_name,
            "querent_notes": self.querent_notes,
            "readings": [r.to_dict() for r in self.readings],
            "status": self.status,
            "purpose": self.purpose,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConsultationSession':
        """Deserialize from JSON storage."""
        readings_data = data.pop("readings", [])
        session = cls(**data)
        session.readings = [
            ReadingRecord.from_dict(r) if isinstance(r, dict) else r
            for r in readings_data
        ]
        return session


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class SessionManager:
    """
    Manages session lifecycle and persistence.

    Handles creating, loading, saving, archiving, and listing sessions.
    Sessions are stored as JSON files in ~/.yijing/sessions/.
    """

    def __init__(self, sessions_dir: Optional[Path] = None):
        """
        Initialize the session manager.

        Args:
            sessions_dir: Directory for session files (default: ~/.yijing/sessions)
        """
        self.sessions_dir = sessions_dir or Path.home() / ".yijing" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        # Archived sessions subdirectory
        self.archived_dir = self.sessions_dir / "archived"
        self.archived_dir.mkdir(exist_ok=True)

        # Active session tracking
        self.active_session_id: Optional[str] = None
        self._load_active_session_id()

    def create_session(
        self,
        name: Optional[str] = None,
        querent_name: Optional[str] = None,
        purpose: str = ""
    ) -> ConsultationSession:
        """
        Create a new consultation session.

        Args:
            name: Human-readable session name
            querent_name: Optional querent name
            purpose: Why the session was started

        Returns:
            The newly created ConsultationSession
        """
        # Generate short ID for CLI friendliness
        session_id = str(uuid.uuid4())[:8]
        now = utc_now()

        session = ConsultationSession(
            id=session_id,
            name=name or f"session-{session_id}",
            created_at=now,
            last_accessed=now,
            querent_name=querent_name,
            purpose=purpose,
        )

        self._save_session(session)
        self.set_active_session(session_id)
        return session

    def get_session(self, session_id: str) -> Optional[ConsultationSession]:
        """
        Load a session by ID.

        Args:
            session_id: The session's short UUID

        Returns:
            The ConsultationSession or None if not found
        """
        # Check active sessions
        path = self.sessions_dir / f"{session_id}.json"
        if path.exists():
            try:
                data = json.loads(path.read_text())
                return ConsultationSession.from_dict(data)
            except (json.JSONDecodeError, IOError):
                return None

        # Check archived sessions
        archived_path = self.archived_dir / f"{session_id}.json"
        if archived_path.exists():
            try:
                data = json.loads(archived_path.read_text())
                return ConsultationSession.from_dict(data)
            except (json.JSONDecodeError, IOError):
                return None

        return None

    def get_active_session(self) -> Optional[ConsultationSession]:
        """
        Get the currently active session.

        Returns:
            The active ConsultationSession or None
        """
        if not self.active_session_id:
            return None
        return self.get_session(self.active_session_id)

    def set_active_session(self, session_id: str) -> None:
        """
        Set the active session.

        Args:
            session_id: The session to make active
        """
        self.active_session_id = session_id
        self._save_active_session_id()

    def clear_active_session(self) -> None:
        """Clear the active session marker."""
        self.active_session_id = None
        self._save_active_session_id()

    def save_session(self, session: ConsultationSession) -> None:
        """
        Save a session to disk.

        Args:
            session: The session to save
        """
        self._save_session(session)

    def list_sessions(
        self,
        status: Optional[str] = None,
        include_archived: bool = False
    ) -> List[ConsultationSession]:
        """
        List all sessions, optionally filtered by status.

        Args:
            status: Filter by session status
            include_archived: Include archived sessions

        Returns:
            List of sessions, sorted by last_accessed (newest first)
        """
        sessions = []

        # Active sessions
        for path in self.sessions_dir.glob("*.json"):
            if path.name == "_active.json":
                continue
            try:
                data = json.loads(path.read_text())
                session = ConsultationSession.from_dict(data)
                if status is None or session.status == status:
                    sessions.append(session)
            except (json.JSONDecodeError, IOError):
                continue

        # Archived sessions
        if include_archived:
            for path in self.archived_dir.glob("*.json"):
                try:
                    data = json.loads(path.read_text())
                    session = ConsultationSession.from_dict(data)
                    if status is None or session.status == status:
                        sessions.append(session)
                except (json.JSONDecodeError, IOError):
                    continue

        return sorted(sessions, key=lambda s: s.last_accessed, reverse=True)

    def archive_session(self, session_id: str) -> bool:
        """
        Archive a session (mark as no longer active).

        Args:
            session_id: The session to archive

        Returns:
            True if archived successfully
        """
        session = self.get_session(session_id)
        if not session:
            return False

        # Update status
        session.status = "archived"

        # Move file to archived directory
        source = self.sessions_dir / f"{session_id}.json"
        dest = self.archived_dir / f"{session_id}.json"

        if source.exists():
            dest.write_text(json.dumps(session.to_dict(), indent=2, ensure_ascii=False))
            source.unlink()

        # Clear if was active
        if self.active_session_id == session_id:
            self.clear_active_session()

        return True

    def delete_session(self, session_id: str) -> bool:
        """
        Permanently delete a session.

        Args:
            session_id: The session to delete

        Returns:
            True if deleted successfully
        """
        for directory in [self.sessions_dir, self.archived_dir]:
            path = directory / f"{session_id}.json"
            if path.exists():
                path.unlink()
                if self.active_session_id == session_id:
                    self.clear_active_session()
                return True
        return False

    def _save_session(self, session: ConsultationSession) -> None:
        """Internal: persist session to disk."""
        # Determine directory based on status
        if session.status == "archived":
            directory = self.archived_dir
        else:
            directory = self.sessions_dir

        path = directory / f"{session.id}.json"
        path.write_text(json.dumps(session.to_dict(), indent=2, ensure_ascii=False))

    def _load_active_session_id(self) -> None:
        """Internal: load active session ID from marker file."""
        path = self.sessions_dir / "_active.json"
        if path.exists():
            try:
                data = json.loads(path.read_text())
                self.active_session_id = data.get("active_session_id")
            except (json.JSONDecodeError, IOError):
                self.active_session_id = None

    def _save_active_session_id(self) -> None:
        """Internal: save active session ID to marker file."""
        path = self.sessions_dir / "_active.json"
        path.write_text(json.dumps({
            "active_session_id": self.active_session_id
        }, indent=2))


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def display_session_list(sessions: List[ConsultationSession], active_id: Optional[str] = None) -> str:
    """
    Generate ASCII display of session list.

    Args:
        sessions: List of sessions to display
        active_id: ID of the currently active session

    Returns:
        Formatted string for terminal output
    """
    if not sessions:
        return "No sessions found."

    lines = []
    lines.append("╔════════════════════════════════════════════════════════════════════════╗")
    lines.append("║                         CONSULTATION SESSIONS                          ║")
    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    for session in sessions:
        active_marker = " *" if session.id == active_id else "  "
        status_marker = "📁" if session.status == "archived" else "📖"

        # Format: [ID] Name (N readings) - status
        header = f"{status_marker}{active_marker} [{session.id}] {session.name}"
        reading_count = f"({len(session.readings)} readings)"
        line = f"║  {header[:45].ljust(45)} {reading_count:>15}  ║"
        lines.append(line)

        # Last accessed
        last = session.last_accessed[:10] if session.last_accessed else "unknown"
        lines.append(f"║      Last accessed: {last.ljust(49)}║")

    lines.append("╚════════════════════════════════════════════════════════════════════════╝")

    if active_id:
        lines.append(f"\n  * = Active session ({active_id})")

    return "\n".join(lines)


def display_session_history(session: ConsultationSession) -> str:
    """
    Generate ASCII display of session reading history.

    Args:
        session: The session to display

    Returns:
        Formatted string for terminal output
    """
    lines = []
    lines.append("╔════════════════════════════════════════════════════════════════════════╗")
    lines.append(f"║  SESSION: {session.name[:60].ljust(60)}  ║")
    lines.append(f"║  ID: {session.id}  |  Readings: {len(session.readings)}".ljust(73) + "║")
    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    if not session.readings:
        lines.append("║  No readings yet.                                                      ║")
    else:
        for i, reading in enumerate(session.readings, 1):
            # Hexagram info
            chinese = reading.primary_name.get("chinese", "?")
            pinyin = reading.primary_name.get("pinyin", "?")
            english = reading.primary_name.get("english", "?")

            hex_info = f"#{reading.primary_hexagram} {chinese} {pinyin}"
            lines.append(f"║  {i}. {hex_info[:30].ljust(30)} {reading.timestamp[:10]:>20}      ║")

            # Question (truncated)
            q = reading.question[:60] if reading.question else "(no question)"
            lines.append(f"║     Q: {q.ljust(64)}║")

            # Moving lines
            if reading.moving_lines:
                ml = ", ".join(str(m) for m in reading.moving_lines)
                lines.append(f"║     Moving: {ml.ljust(58)}║")

            # Outcome
            if reading.outcome != "pending":
                lines.append(f"║     Outcome: {reading.outcome.ljust(57)}║")

            if i < len(session.readings):
                lines.append("║  ────────────────────────────────────────────────────────────────────  ║")

    lines.append("╚════════════════════════════════════════════════════════════════════════╝")

    return "\n".join(lines)


def display_pattern_analysis(patterns: PatternAnalysis, session_name: str = "") -> str:
    """
    Generate ASCII display of pattern analysis.

    Args:
        patterns: The pattern analysis to display
        session_name: Optional session name for header

    Returns:
        Formatted string for terminal output
    """
    lines = []
    lines.append("╔════════════════════════════════════════════════════════════════════════╗")
    header = f"PATTERN ANALYSIS: {session_name}" if session_name else "PATTERN ANALYSIS"
    lines.append(f"║  {header[:68].ljust(68)}  ║")
    lines.append(f"║  ({patterns.reading_count} readings analyzed)".ljust(73) + "║")
    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    # Recurring trigrams
    lines.append("║  RECURRING TRIGRAMS (3+ appearances):".ljust(73) + "║")
    if patterns.recurring_trigrams:
        for trig in patterns.recurring_trigrams:
            count = patterns.trigram_frequencies.get(trig, 0)
            lines.append(f"║    • {trig}: {count}x".ljust(73) + "║")
    else:
        lines.append("║    (none)".ljust(73) + "║")

    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    # Element balance
    lines.append("║  ELEMENTAL BALANCE:".ljust(73) + "║")
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        status = patterns.element_balance.get(elem, "balanced")
        count = patterns.element_frequencies.get(elem, 0)

        if status == "excess":
            symbol = "▲ excess"
        elif status == "deficient":
            symbol = "▽ deficient"
        else:
            symbol = "─ balanced"

        lines.append(f"║    {elem:8} ({count:2}): {symbol}".ljust(73) + "║")

    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    # Recurring hexagrams
    lines.append("║  RECURRING HEXAGRAMS (2+ appearances):".ljust(73) + "║")
    if patterns.recurring_hexagrams:
        for hex_num in patterns.recurring_hexagrams[:5]:  # Limit to 5
            count = patterns.hexagram_frequencies.get(hex_num, 0)
            name = HEXAGRAM_NAMES.get(hex_num, ("?", "?", "?"))
            lines.append(f"║    • #{hex_num} {name[0]} {name[1]}: {count}x".ljust(73) + "║")
    else:
        lines.append("║    (none)".ljust(73) + "║")

    lines.append("╠════════════════════════════════════════════════════════════════════════╣")

    # Moving line positions
    lines.append("║  MOVING LINE FREQUENCY:".ljust(73) + "║")
    max_count = max(patterns.moving_line_positions.values()) if patterns.moving_line_positions else 1
    for pos in range(1, 7):
        count = patterns.moving_line_positions.get(pos, 0)
        bar_len = int((count / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_len + "░" * (20 - bar_len)
        lines.append(f"║    Line {pos}: {bar} ({count})".ljust(73) + "║")

    lines.append("╚════════════════════════════════════════════════════════════════════════╝")

    # Insights
    insights = patterns.get_insights()
    if insights:
        lines.append("\n  INSIGHTS:")
        for insight in insights:
            lines.append(f"  • {insight}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN (for testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Simple test
    manager = SessionManager()

    print("Creating test session...")
    session = manager.create_session(name="Test Session", purpose="Testing session management")
    print(f"Created session: {session.id}")

    # List sessions
    sessions = manager.list_sessions()
    print(display_session_list(sessions, manager.active_session_id))

    print("\nSession history:")
    print(display_session_history(session))

    # Cleanup
    manager.delete_session(session.id)
    print(f"\nDeleted test session: {session.id}")
