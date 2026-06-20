#!/usr/bin/env python3
"""
Horary Chart Data Utilities

This module provides utilities for fetching and formatting horary chart data.
Since most astrology sites don't have public APIs, this provides:
1. Guidance on obtaining chart data from free online services
2. A structured format for chart data input
3. Utilities for parsing and validating chart information

RECOMMENDED FREE CHART SERVICES:
- Astro.com (astro.com/cgi/chart.cgi) - Best for professional charts
- Astro-seek.com (astro-seek.com/horary-astrology-chart) - Has horary-specific features
- Cafe Astrology (cafeastrology.com/free-natal-chart-report.html) - Quick charts

For programmatic access, consider:
- Swiss Ephemeris (pyswisseph): pip install pyswisseph
- Kerykeion: pip install kerykeion (modern Python astrology library)
- Flatlib: Traditional astrology library
"""

import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

# Traditional rulerships (no outer planets)
TRADITIONAL_RULERS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter"
}

PLANETARY_HOURS_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
DAY_RULERS = {
    0: "Moon",      # Monday
    1: "Mars",      # Tuesday
    2: "Mercury",   # Wednesday
    3: "Jupiter",   # Thursday
    4: "Venus",     # Friday
    5: "Saturn",    # Saturday
    6: "Sun"        # Sunday
}

@dataclass
class PlanetPosition:
    """Position of a planet in the horary chart."""
    planet: str
    sign: str
    degree: float
    minute: int = 0
    retrograde: bool = False
    house: Optional[int] = None

    @property
    def full_position(self) -> str:
        r = "R" if self.retrograde else ""
        return f"{self.planet} {self.degree:.0f}°{self.minute:02d}' {self.sign}{r}"

    @property
    def absolute_degree(self) -> float:
        """Convert to absolute zodiacal degree (0-360)."""
        sign_starts = {
            "Aries": 0, "Taurus": 30, "Gemini": 60, "Cancer": 90,
            "Leo": 120, "Virgo": 150, "Libra": 180, "Scorpio": 210,
            "Sagittarius": 240, "Capricorn": 270, "Aquarius": 300, "Pisces": 330
        }
        return sign_starts.get(self.sign, 0) + self.degree + (self.minute / 60)

@dataclass
class HouseCusp:
    """House cusp position."""
    house: int
    sign: str
    degree: float
    minute: int = 0

    @property
    def ruler(self) -> str:
        """Return the traditional ruler of this house cusp sign."""
        return TRADITIONAL_RULERS.get(self.sign, "Unknown")

@dataclass
class HoraryChart:
    """Complete horary chart data structure."""
    question: str
    datetime_utc: str
    location: str
    latitude: float
    longitude: float

    planets: list = field(default_factory=list)
    houses: list = field(default_factory=list)

    # Optional metadata
    house_system: str = "Regiomontanus"
    day_ruler: str = ""
    hour_ruler: str = ""

    def __post_init__(self):
        # Calculate day ruler if datetime provided
        if self.datetime_utc and not self.day_ruler:
            try:
                dt = datetime.fromisoformat(self.datetime_utc.replace("Z", "+00:00"))
                self.day_ruler = DAY_RULERS.get(dt.weekday(), "")
            except:
                pass

    def get_planet(self, name: str) -> Optional[PlanetPosition]:
        """Get a planet by name."""
        for p in self.planets:
            if isinstance(p, dict):
                if p.get("planet") == name:
                    return PlanetPosition(**p)
            elif hasattr(p, "planet") and p.planet == name:
                return p
        return None

    def get_house_cusp(self, house_num: int) -> Optional[HouseCusp]:
        """Get a house cusp by number."""
        for h in self.houses:
            if isinstance(h, dict):
                if h.get("house") == house_num:
                    return HouseCusp(**h)
            elif hasattr(h, "house") and h.house == house_num:
                return h
        return None

    def get_house_ruler(self, house_num: int) -> str:
        """Get the planetary ruler of a house."""
        cusp = self.get_house_cusp(house_num)
        if cusp:
            return cusp.ruler
        return "Unknown"

    def to_json(self) -> str:
        """Export chart as JSON."""
        data = {
            "question": self.question,
            "datetime_utc": self.datetime_utc,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "house_system": self.house_system,
            "day_ruler": self.day_ruler,
            "hour_ruler": self.hour_ruler,
            "planets": [asdict(p) if hasattr(p, "__dataclass_fields__") else p for p in self.planets],
            "houses": [asdict(h) if hasattr(h, "__dataclass_fields__") else h for h in self.houses]
        }
        return json.dumps(data, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "HoraryChart":
        """Import chart from JSON."""
        data = json.loads(json_str)
        planets = [PlanetPosition(**p) for p in data.pop("planets", [])]
        houses = [HouseCusp(**h) for h in data.pop("houses", [])]
        chart = cls(**data)
        chart.planets = planets
        chart.houses = houses
        return chart


def create_sample_chart() -> HoraryChart:
    """Create a sample chart structure for reference."""
    chart = HoraryChart(
        question="Will I get this job?",
        datetime_utc="2026-01-11T14:30:00Z",
        location="London, UK",
        latitude=51.5074,
        longitude=-0.1278,
        house_system="Regiomontanus"
    )

    # Sample planets
    chart.planets = [
        PlanetPosition("Sun", "Capricorn", 21, 15, False, 10),
        PlanetPosition("Moon", "Gemini", 15, 30, False, 3),
        PlanetPosition("Mercury", "Capricorn", 5, 45, True, 9),
        PlanetPosition("Venus", "Pisces", 10, 20, False, 11),
        PlanetPosition("Mars", "Cancer", 25, 10, False, 4),
        PlanetPosition("Jupiter", "Gemini", 12, 0, False, 3),
        PlanetPosition("Saturn", "Pisces", 28, 55, False, 12),
    ]

    # Sample houses
    chart.houses = [
        HouseCusp(1, "Aries", 15, 30),
        HouseCusp(2, "Taurus", 18, 45),
        HouseCusp(3, "Gemini", 12, 20),
        HouseCusp(4, "Cancer", 5, 10),
        HouseCusp(5, "Leo", 2, 30),
        HouseCusp(6, "Virgo", 8, 15),
        HouseCusp(7, "Libra", 15, 30),
        HouseCusp(8, "Scorpio", 18, 45),
        HouseCusp(9, "Sagittarius", 12, 20),
        HouseCusp(10, "Capricorn", 5, 10),
        HouseCusp(11, "Aquarius", 2, 30),
        HouseCusp(12, "Pisces", 8, 15),
    ]

    return chart


def print_chart_template():
    """Print a template for manually entering chart data."""
    template = """
HORARY CHART DATA TEMPLATE
==========================

When providing chart data, include:

1. QUESTION
   "Your specific question here"

2. DATE/TIME/LOCATION
   Date: YYYY-MM-DD
   Time: HH:MM (24-hour, local time)
   Timezone: (e.g., UTC, EST, PST)
   Location: City, Country
   Coordinates: Latitude, Longitude (optional if city provided)

3. PLANETARY POSITIONS
   Format: Planet Sign Degree°Minute' [R for retrograde] [House]

   Example:
   Sun     Capricorn  21°15'      10th
   Moon    Gemini     15°30'      3rd
   Mercury Capricorn   5°45' R    9th
   Venus   Pisces     10°20'      11th
   Mars    Cancer     25°10'      4th
   Jupiter Gemini     12°00'      3rd
   Saturn  Pisces     28°55'      12th

4. HOUSE CUSPS
   Format: House Sign Degree°Minute'

   Example:
   ASC (1st)  Aries    15°30'
   2nd        Taurus   18°45'
   3rd        Gemini   12°20'
   IC (4th)   Cancer    5°10'
   5th        Leo       2°30'
   6th        Virgo     8°15'
   DSC (7th)  Libra    15°30'
   8th        Scorpio  18°45'
   9th        Sagittarius 12°20'
   MC (10th)  Capricorn  5°10'
   11th       Aquarius   2°30'
   12th       Pisces     8°15'

5. ADDITIONAL INFO (optional)
   House System: Regiomontanus/Placidus
   Day Ruler: (planet ruling the day)
   Hour Ruler: (planet ruling the hour)

---

FREE CHART SERVICES:

1. Astro.com - https://www.astro.com/cgi/chart.cgi
   - Select "Horary Chart" under chart type
   - Enter date/time/location of question
   - Use Regiomontanus houses

2. Astro-seek.com - https://horoscopes.astro-seek.com/horary-astrology-chart-online
   - Specifically designed for horary
   - Shows traditional rulers

3. For programmatic access, install:
   pip install kerykeion

   Then use:
   from kerykeion import AstrologicalSubject
   chart = AstrologicalSubject("Horary", 2026, 1, 11, 14, 30, "London")
"""
    print(template)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--template":
        print_chart_template()
    elif len(sys.argv) > 1 and sys.argv[1] == "--sample":
        chart = create_sample_chart()
        print("Sample Horary Chart:")
        print("=" * 50)
        print(f"Question: {chart.question}")
        print(f"Time: {chart.datetime_utc}")
        print(f"Location: {chart.location}")
        print(f"Day Ruler: {chart.day_ruler}")
        print()
        print("Planets:")
        for p in chart.planets:
            print(f"  {p.full_position} (House {p.house})")
        print()
        print("Houses:")
        for h in chart.houses:
            print(f"  House {h.house}: {h.degree}°{h.minute:02d}' {h.sign} (ruler: {h.ruler})")
        print()
        print("JSON Export:")
        print(chart.to_json())
    else:
        print("Horary Chart Data Utilities")
        print()
        print("Usage:")
        print("  python chart_data.py --template   Show data entry template")
        print("  python chart_data.py --sample     Show sample chart structure")
        print()
        print("For horary readings, provide chart data to Claude using")
        print("the template format, or calculate using free online services.")
