# Lab 7: Fuzz Testing for Input Validation Bugs

**Student Name:** Pradyumn Bidari  
**SRN:** PES1UG24AM194  
**Project:** Pet Walking Service  
**Assigned Repository:** https://github.com/SETAPESU26/L6_L7_13_pet_walking_service

## Objective

Use the Hypothesis library to find and fix input-validation bugs in a Python application through property-based fuzz testing.

## Files

| File | Purpose |
| --- | --- |
| `processor.py` | Fixed application that validates pet-walking inputs. |
| `test_processor.py` | Hypothesis fuzz tests and edge-case checks for all three functions. |
| `Lab_7_Fuzz_Testing_Report_Pradyumn_Bidari.pdf` | Before-and-after test output captures and results. |
| `README.md` | Lab instructions and project summary. |

## Requirements

- Python 3.8 or newer
- `pytest`
- `hypothesis`

Install the test dependencies:

```bash
python -m pip install pytest hypothesis
```

## How to Run

Open a terminal in the `Lab 7` folder.

Run the application:

```bash
python processor.py
```

Example inputs:

```text
2-30-YES
45/3
PLAYFUL
```

Run the fuzz tests:

```bash
python -m pytest test_processor.py -v
```

## Functions Tested

1. **`parse_walk_schedule()`** - Checks schedule format, positive pet count, positive minutes, and YES/NO weekend values.
2. **`compute_pace_per_pet()`** - Rejects invalid numbers, division by zero, negative values, NaN, and infinity.
3. **`lookup_temperament_surcharge()`** - Supports valid temperament codes and full names; rejects unknown values.

## Test Results

| Version | Result |
| --- | --- |
| Original buggy code | 38 failed, 2 passed |
| Fixed code | **40 passed** |

Hypothesis also generates numerous random inputs within the property-based tests to check unexpected edge cases. The updated code handles invalid inputs without raising exceptions.

## Submission

Upload `processor.py`, `test_processor.py`, `Lab_7_Fuzz_Testing_Report_Pradyumn_Bidari.pdf`, and this `README.md` to the repository's `Lab 7` folder.
