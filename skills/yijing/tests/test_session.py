#!/usr/bin/env python3
"""
Session Management Test Suite

Tests verify the session persistence and pattern detection systems:
- Session creation, persistence, and retrieval
- Reading record serialization
- Pattern analysis across multiple readings
- Session state transitions

Run with: python -m pytest .claude/skills/yijing/tests/test_session.py -v
Or:       python .claude/skills/yijing/tests/test_session.py
"""

import json
import sys
import tempfile
import shutil
import uuid
from pathlib import Path

# Add script directory to path
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

from session import (
    ReadingRecord,
    PatternAnalysis,
    ConsultationSession,
    SessionManager,
    utc_now,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

def create_test_reading(
    hexagram: int = 11,
    question: str = "Test question",
    moving_lines: list = None,
    lower_trigram_name: str = "Qian",
    upper_trigram_name: str = "Kun",
    lower_element: str = "Metal",
    upper_element: str = "Earth",
) -> ReadingRecord:
    """Create a test reading record."""
    if moving_lines is None:
        moving_lines = [2, 5]

    # Build trigram dicts matching the actual structure
    lower_trigram = {
        "name": lower_trigram_name,
        "symbol": "☰" if lower_trigram_name == "Qian" else "☷",
        "element": lower_element,
        "image": "Heaven" if lower_trigram_name == "Qian" else "Earth",
    }
    upper_trigram = {
        "name": upper_trigram_name,
        "symbol": "☷" if upper_trigram_name == "Kun" else "☰",
        "element": upper_element,
        "image": "Earth" if upper_trigram_name == "Kun" else "Heaven",
    }

    return ReadingRecord(
        id=f"test-reading-{uuid.uuid4().hex[:8]}",
        timestamp=utc_now(),
        question=question,
        primary_hexagram=hexagram,
        primary_name={"chinese": "泰", "pinyin": "Tài", "english": "Peace"},
        lines=[
            {"position": 1, "value": 7, "is_yang": True, "is_moving": False},
            {"position": 2, "value": 6, "is_yang": False, "is_moving": 2 in moving_lines},
            {"position": 3, "value": 7, "is_yang": True, "is_moving": False},
            {"position": 4, "value": 8, "is_yang": False, "is_moving": False},
            {"position": 5, "value": 9, "is_yang": True, "is_moving": 5 in moving_lines},
            {"position": 6, "value": 8, "is_yang": False, "is_moving": False},
        ],
        moving_lines=moving_lines,
        lower_trigram=lower_trigram,
        upper_trigram=upper_trigram,
        nuclear_hexagram=54,
        relating_hexagram=12 if moving_lines else None,
        method="yarrow",
        seed=42,
    )


class TempSessionManager:
    """Context manager for testing with temporary session directory."""

    def __init__(self):
        self.temp_dir = None
        self.manager = None

    def __enter__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.manager = SessionManager(sessions_dir=self.temp_dir)
        return self.manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# READING RECORD TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_reading_record_creation() -> None:
    """Test basic reading record creation."""
    reading = create_test_reading()

    assert reading.primary_hexagram == 11
    assert reading.moving_lines == [2, 5]
    assert reading.method == "yarrow"
    assert reading.seed == 42
    assert len(reading.lines) == 6

    print("✓ Reading record creation verified")


def test_reading_record_serialization() -> None:
    """Test reading record to/from dict conversion."""
    original = create_test_reading()
    data = original.to_dict()

    # Verify structure
    assert 'id' in data
    assert 'timestamp' in data
    assert 'question' in data
    assert 'primary_hexagram' in data
    assert 'lines' in data
    assert 'moving_lines' in data

    # Roundtrip
    restored = ReadingRecord.from_dict(data)
    assert restored.primary_hexagram == original.primary_hexagram
    assert restored.moving_lines == original.moving_lines
    assert restored.question == original.question

    print("✓ Reading record serialization verified")


def test_reading_no_moving_lines() -> None:
    """Test reading with no moving lines has no relating hexagram."""
    reading = create_test_reading(moving_lines=[])

    assert reading.moving_lines == []
    assert reading.relating_hexagram is None

    print("✓ Reading without moving lines verified")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSULTATION SESSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_session_creation() -> None:
    """Test consultation session creation."""
    session = ConsultationSession(
        id="test-session-001",
        name="Test Consultation",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[],
    )

    assert session.id == "test-session-001"
    assert session.name == "Test Consultation"
    assert session.readings == []
    assert session.status == "active"

    print("✓ Consultation session creation verified")


def test_session_add_reading() -> None:
    """Test adding readings to a session."""
    session = ConsultationSession(
        id="test-session-002",
        name="Multi-reading Test",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[],
    )

    reading1 = create_test_reading(hexagram=11, question="First question")
    reading2 = create_test_reading(hexagram=64, question="Second question")

    session.add_reading(reading1)
    session.add_reading(reading2)

    assert len(session.readings) == 2
    assert session.readings[0].primary_hexagram == 11
    assert session.readings[1].primary_hexagram == 64

    print("✓ Adding readings to session verified")


def test_session_serialization() -> None:
    """Test session to/from dict conversion."""
    session = ConsultationSession(
        id="test-session-003",
        name="Serialization Test",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[create_test_reading()],
    )

    data = session.to_dict()
    assert 'id' in data
    assert 'name' in data
    assert 'readings' in data
    assert len(data['readings']) == 1

    restored = ConsultationSession.from_dict(data)
    assert restored.id == session.id
    assert restored.name == session.name
    assert len(restored.readings) == 1

    print("✓ Session serialization verified")


# ═══════════════════════════════════════════════════════════════════════════════
# PATTERN ANALYSIS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_pattern_detection_trigrams() -> None:
    """Test trigram frequency detection."""
    session = ConsultationSession(
        id="pattern-test-001",
        name="Pattern Test",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[
            create_test_reading(lower_trigram_name="Qian", upper_trigram_name="Kun"),
            create_test_reading(lower_trigram_name="Qian", upper_trigram_name="Li"),
            create_test_reading(lower_trigram_name="Qian", upper_trigram_name="Kan"),
            create_test_reading(lower_trigram_name="Zhen", upper_trigram_name="Qian"),
        ],
    )

    patterns = session.get_patterns()

    # Qian appears 4 times (3 as lower, 1 as upper)
    assert patterns.trigram_frequencies.get("Qian", 0) == 4
    assert "Qian" in patterns.recurring_trigrams  # 3+ appearances

    print("✓ Trigram frequency detection verified")


def test_pattern_detection_elements() -> None:
    """Test element balance detection."""
    session = ConsultationSession(
        id="pattern-test-002",
        name="Element Test",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[
            create_test_reading(lower_element="Metal", upper_element="Metal"),
            create_test_reading(lower_element="Metal", upper_element="Water"),
            create_test_reading(lower_element="Wood", upper_element="Metal"),
        ],
    )

    patterns = session.get_patterns()

    # Metal should appear 4 times (dominant)
    assert patterns.element_frequencies.get("Metal", 0) == 4
    assert patterns.element_frequencies.get("Wood", 0) == 1
    assert patterns.element_frequencies.get("Water", 0) == 1

    print("✓ Element frequency detection verified")


def test_pattern_moving_line_positions() -> None:
    """Test moving line position tracking."""
    session = ConsultationSession(
        id="pattern-test-003",
        name="Moving Lines Test",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[
            create_test_reading(moving_lines=[2, 5]),
            create_test_reading(moving_lines=[2, 3]),
            create_test_reading(moving_lines=[5, 6]),
        ],
    )

    patterns = session.get_patterns()

    # Position 2 appears 2 times, position 5 appears 2 times
    assert patterns.moving_line_positions.get(2, 0) == 2
    assert patterns.moving_line_positions.get(5, 0) == 2
    assert patterns.moving_line_positions.get(3, 0) == 1
    assert patterns.moving_line_positions.get(6, 0) == 1

    print("✓ Moving line position tracking verified")


def test_pattern_recurring_hexagrams() -> None:
    """Test recurring hexagram detection."""
    session = ConsultationSession(
        id="pattern-test-004",
        name="Recurring Hexagrams",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[
            create_test_reading(hexagram=11),
            create_test_reading(hexagram=64),
            create_test_reading(hexagram=11),  # 11 appears twice
        ],
    )

    patterns = session.get_patterns()

    assert 11 in patterns.recurring_hexagrams  # Appears 2+ times

    print("✓ Recurring hexagram detection verified")


def test_empty_session_patterns() -> None:
    """Test pattern analysis on empty session."""
    session = ConsultationSession(
        id="empty-test",
        name="Empty Session",
        created_at=utc_now(),
        last_accessed=utc_now(),
        readings=[],
    )

    patterns = session.get_patterns()

    assert patterns.trigram_frequencies == {}
    assert patterns.element_frequencies == {}
    assert patterns.recurring_trigrams == []
    assert patterns.recurring_hexagrams == []

    print("✓ Empty session pattern analysis verified")


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION MANAGER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_manager_create_session() -> None:
    """Test session manager creates and persists sessions."""
    with TempSessionManager() as manager:
        session = manager.create_session("Test Session")

        assert session.name == "Test Session"
        assert session.status == "active"

        # Verify file was created
        session_file = Path(manager.sessions_dir) / f"{session.id}.json"
        assert session_file.exists()

        print("✓ Session manager creation verified")


def test_manager_get_session() -> None:
    """Test session retrieval by ID."""
    with TempSessionManager() as manager:
        created = manager.create_session("Retrieval Test")

        retrieved = manager.get_session(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name

        print("✓ Session retrieval verified")


def test_manager_get_active() -> None:
    """Test active session tracking."""
    with TempSessionManager() as manager:
        # Initially no active session
        assert manager.get_active_session() is None

        # Create session
        session = manager.create_session("Active Test")

        # Should now be active
        active = manager.get_active_session()
        assert active is not None
        assert active.id == session.id

        print("✓ Active session tracking verified")


def test_manager_list_sessions() -> None:
    """Test listing all sessions."""
    with TempSessionManager() as manager:
        manager.create_session("Session A")
        manager.create_session("Session B")
        manager.create_session("Session C")

        sessions = manager.list_sessions()

        assert len(sessions) == 3
        names = {s.name for s in sessions}
        assert "Session A" in names
        assert "Session B" in names
        assert "Session C" in names

        print("✓ Session listing verified")


def test_manager_archive_session() -> None:
    """Test session archival."""
    with TempSessionManager() as manager:
        session = manager.create_session("Archive Test")
        session_id = session.id

        manager.archive_session(session_id)

        # Verify archived status
        archived = manager.get_session(session_id)
        assert archived.status == "archived"

        # Verify active session cleared
        assert manager.get_active_session() is None

        print("✓ Session archival verified")


def test_manager_add_reading_to_session() -> None:
    """Test adding readings to a session and saving."""
    with TempSessionManager() as manager:
        session = manager.create_session("Reading Test")
        reading = create_test_reading()

        # Add reading to session and save
        session.add_reading(reading)
        manager.save_session(session)

        # Retrieve and verify
        retrieved = manager.get_session(session.id)
        assert len(retrieved.readings) == 1
        assert retrieved.readings[0].primary_hexagram == 11

        print("✓ Adding readings to session verified")


def test_manager_persistence() -> None:
    """Test session data persists across manager instances."""
    with TempSessionManager() as manager:
        session = manager.create_session("Persistence Test")
        reading = create_test_reading(question="Persistent question")
        session.add_reading(reading)
        manager.save_session(session)

        # Create new manager with same directory
        manager2 = SessionManager(sessions_dir=manager.sessions_dir)
        retrieved = manager2.get_session(session.id)

        assert retrieved is not None
        assert len(retrieved.readings) == 1
        assert retrieved.readings[0].question == "Persistent question"

        print("✓ Cross-instance persistence verified")


# ═══════════════════════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════

def test_nonexistent_session() -> None:
    """Test retrieving non-existent session returns None."""
    with TempSessionManager() as manager:
        result = manager.get_session("nonexistent-id")
        assert result is None

        print("✓ Non-existent session handling verified")


def test_session_name_special_characters() -> None:
    """Test session names with special characters."""
    with TempSessionManager() as manager:
        session = manager.create_session("Career & Life 2026: Questions?!")

        retrieved = manager.get_session(session.id)
        assert retrieved.name == "Career & Life 2026: Questions?!"

        print("✓ Special character session names verified")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("SESSION MANAGEMENT TEST SUITE")
    print("=" * 70)
    print()

    # Reading record tests
    print("Reading Records:")
    test_reading_record_creation()
    test_reading_record_serialization()
    test_reading_no_moving_lines()
    print()

    # Consultation session tests
    print("Consultation Sessions:")
    test_session_creation()
    test_session_add_reading()
    test_session_serialization()
    print()

    # Pattern analysis tests
    print("Pattern Analysis:")
    test_pattern_detection_trigrams()
    test_pattern_detection_elements()
    test_pattern_moving_line_positions()
    test_pattern_recurring_hexagrams()
    test_empty_session_patterns()
    print()

    # Session manager tests
    print("Session Manager:")
    test_manager_create_session()
    test_manager_get_session()
    test_manager_get_active()
    test_manager_list_sessions()
    test_manager_archive_session()
    test_manager_add_reading_to_session()
    test_manager_persistence()
    print()

    # Edge cases
    print("Edge Cases:")
    test_nonexistent_session()
    test_session_name_special_characters()
    print()

    print("=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
