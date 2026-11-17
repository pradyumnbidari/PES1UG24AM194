"""Lab 7: Hypothesis fuzz tests for the pet-walking service.

Student: Pradyumn Bidari (PES1UG24AM194)
Run: python -m pytest test_processor.py -v
"""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import (
    compute_pace_per_pet,
    lookup_temperament_surcharge,
    parse_walk_schedule,
)


# Fuzz unexpected data types and Unicode text, including None.
FUZZ_INPUTS = st.one_of(
    st.text(max_size=150),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.lists(st.integers(), max_size=4),
)


@settings(max_examples=150, deadline=None)
@given(FUZZ_INPUTS)
def test_parse_walk_schedule_no_crash(value):
    """Malformed data must produce a message, never an exception."""
    try:
        result = parse_walk_schedule(value)
    except Exception as exc:
        pytest.fail(f"parse_walk_schedule crashed: {exc!r}")
    assert isinstance(result, str)


@settings(max_examples=150, deadline=None)
@given(FUZZ_INPUTS)
def test_compute_pace_per_pet_safe(value):
    """A pace is either a finite number or None for invalid input."""
    try:
        result = compute_pace_per_pet(value)
    except Exception as exc:
        pytest.fail(f"compute_pace_per_pet crashed: {exc!r}")
    assert result is None or (isinstance(result, float) and math.isfinite(result))


@settings(max_examples=150, deadline=None)
@given(FUZZ_INPUTS)
def test_lookup_temperament_surcharge_safe(value):
    """Unknown temperament inputs must not crash the application."""
    try:
        result = lookup_temperament_surcharge(value)
    except Exception as exc:
        pytest.fail(f"lookup_temperament_surcharge crashed: {exc!r}")
    assert result is None or result in (0.0, 5.0, 12.0, 20.0)


@settings(max_examples=100, deadline=None)
@given(
    pets=st.integers(min_value=1, max_value=100),
    minutes=st.integers(min_value=1, max_value=240),
    weekend=st.booleans(),
)
def test_valid_walk_schedule_fee(pets, minutes, weekend):
    """Fuzz the fee formula, including the 30-minute boundary."""
    weekend_code = "YES" if weekend else "NO"
    actual = parse_walk_schedule(f" {pets}-{minutes}-{weekend_code.lower()} ")
    total = (20.0 if minutes <= 30 else 35.0) + pets * 5.0
    if weekend:
        total += 15.0
    assert actual == f"Walk: {pets} pets, {minutes} mins - Total ${total:.2f}"


@pytest.mark.parametrize(
    "invalid",
    [None, "", "2-30", "2-30-MAYBE", "2--YES", "0-30-YES", "1-0-NO",
     "-1-30-YES", "2-30-YES-extra", "two-30-NO", "2-30-YES!"],
)
def test_invalid_walk_schedule_is_rejected(invalid):
    assert parse_walk_schedule(invalid) == "Invalid walk schedule"


@settings(max_examples=100, deadline=None)
@given(
    minutes=st.integers(min_value=1, max_value=10000),
    pets=st.integers(min_value=1, max_value=100),
)
def test_valid_pace_calculation(minutes, pets):
    assert compute_pace_per_pet(f"{minutes}/{pets}") == round(minutes / pets, 2)


@pytest.mark.parametrize(
    "invalid",
    [None, "", "30", "30/", "/2", "30/0", "-30/2", "30/-2",
     "nan/2", "inf/2", "30/NaN", "1/inf", "1/2/3", "cat/dog"],
)
def test_invalid_pace_returns_none(invalid):
    assert compute_pace_per_pet(invalid) is None


@settings(max_examples=100, deadline=None)
@given(
    name_and_fee=st.sampled_from([
        ("CAL", 0.0), ("CALM", 0.0),
        ("PLY", 5.0), ("PLAYFUL", 5.0),
        ("REA", 12.0), ("REACTIVE", 12.0),
        ("AGG", 20.0), ("AGGRESSIVE", 20.0),
    ]),
    lower_case=st.booleans(),
)
def test_valid_temperament_codes(name_and_fee, lower_case):
    code, expected = name_and_fee
    if lower_case:
        code = code.lower()
    assert lookup_temperament_surcharge(f"  {code}  ") == expected


@pytest.mark.parametrize(
    "invalid",
    [None, "", " ", "UNKNOWN", "CALXYZ", "PLAYTHING", "AGGRO", "123", "CAL!"],
)
def test_invalid_temperament_returns_none(invalid):
    assert lookup_temperament_surcharge(invalid) is None
