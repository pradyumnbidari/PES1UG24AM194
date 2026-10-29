"""Lab 6 - code (line) coverage tests for Pet Walking Service.
Student: Pradyumn Bidari, SRN: PES1UG24AM194.
Run with: py -m coverage run --source=pet_walking_service -m pytest -v CodeCoverageTest_pet_walking_service_application.py
"""

import pytest
from pet_walking_service import inspect_gps_collars, process_walking_routes


def test_standard_30_one_pet():
    routes = [{"route_confirmed": True, "session_type": "standard_30", "walks": [{"num_pets": 1}]}]
    assert process_walking_routes(routes, 5) == {"total_revenue": 27.0, "status": "COMPLETED"}


def test_standard_60_multiple_pets_medication_and_weekend():
    routes = [{"route_confirmed": True, "session_type": "standard_60", "is_weekend": True,
               "walks": [{"num_pets": 4, "needs_meds": True}]}]
    # (35 + 4*8)*0.90 + 6 medication + 5 weekend transport = 71.30
    assert process_walking_routes(routes, 5) == {"total_revenue": 71.3, "status": "COMPLETED"}


def test_express_15_walk():
    routes = [{"route_confirmed": True, "session_type": "express_15", "walks": [{"num_pets": 2}]}]
    assert process_walking_routes(routes, 5)["total_revenue"] == 24.0


def test_invalid_session_counts_incident_and_skips_route():
    routes = [{"route_confirmed": True, "session_type": "overnight", "walks": [{"num_pets": 1}]}]
    assert process_walking_routes(routes, 5) == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_unconfirmed_route_skipped():
    routes = [{"route_confirmed": False, "session_type": "standard_30", "walks": [{"num_pets": 1}]}]
    assert process_walking_routes(routes, 5)["status"] == "ZERO_EARNINGS"


def test_invalid_pet_count_skipped():
    routes = [{"route_confirmed": True, "walks": [{"num_pets": 0}, {"num_pets": 1}]}]
    assert process_walking_routes(routes, 5)["total_revenue"] == 27.0


def test_aggressive_pet_cancels_standard_60_route():
    routes = [{"route_confirmed": True, "session_type": "standard_60", "walks": [
        {"num_pets": 2}, {"num_pets": 1, "aggression_alert": True}, {"num_pets": 1}
    ]}]
    assert process_walking_routes(routes, 5) == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_aggression_non_60_can_add_medication_charge():
    routes = [{"route_confirmed": True, "session_type": "standard_30", "walks": [
        {"num_pets": 1, "aggression_alert": True, "needs_meds": True}
    ]}]
    assert process_walking_routes(routes, 5) == {"total_revenue": 6.0, "status": "COMPLETED"}


def test_over_four_incidents_triggers_audit():
    routes = [{"route_confirmed": True, "walks": [{"num_pets": 0}] * 5}]
    assert process_walking_routes(routes, 5) == {"total_revenue": 0.0, "status": "INCIDENT_AUDIT"}


@pytest.mark.parametrize("routes, fee", [("not-a-list", 5), ([], -1)])
def test_invalid_arguments_raise(routes, fee):
    with pytest.raises(ValueError, match="Invalid routes"):
        process_walking_routes(routes, fee)


def test_gps_no_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_online_for_normal_and_recovered_signal():
    assert inspect_gps_collars([[100, 19, 20, 19], [35, 90]]) == "ONLINE"


def test_gps_lost_after_two_weak_readings():
    assert inspect_gps_collars([[50, 19, 18]]) == "LOST_SIGNAL_ALERT"
