"""Lab 6 - branch coverage tests for Pet Walking Service.
Student: Pradyumn Bidari, SRN: PES1UG24AM194.
Run with: py -m coverage run --branch --source=pet_walking_service -m pytest -v BranchCoverageTest_pet_walking_service_application.py
"""

import pytest
from pet_walking_service import inspect_gps_collars, process_walking_routes


def route(session="standard_30", walks=None, confirmed=True, weekend=False):
    return {"route_confirmed": confirmed, "session_type": session,
            "walks": [] if walks is None else walks, "is_weekend": weekend}


def test_rejects_non_list_and_negative_transport_fees():
    for routes, fee in [(None, 5), ((), 5), ([], -0.01)]:
        with pytest.raises(ValueError, match="Invalid routes list or transport fee"):
            process_walking_routes(routes, fee)


def test_empty_list_or_unconfirmed_route_gives_zero():
    assert process_walking_routes([], 5) == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}
    assert process_walking_routes([route(confirmed=False)], 5)["status"] == "ZERO_EARNINGS"
    assert process_walking_routes([{}], 5)["status"] == "ZERO_EARNINGS"


def test_session_default_is_standard_30_and_defaults_of_walk_fields():
    routes = [{"route_confirmed": True, "walks": [{"num_pets": 1}]}]
    assert process_walking_routes(routes, 5)["total_revenue"] == 27.0
    assert process_walking_routes([{"route_confirmed": True}], 5)["status"] == "ZERO_EARNINGS"


def test_each_valid_session_tier():
    cases = [("standard_60", 40.0), ("standard_30", 27.0), ("express_15", 19.0)]
    for session, expected in cases:
        assert process_walking_routes([route(session, [{"num_pets": 1}])], 5)["total_revenue"] == expected


def test_unknown_session_skipped_even_when_weekend():
    assert process_walking_routes([route("unknown", [{"num_pets": 1}], weekend=True)], 5) == {
        "total_revenue": 0.0, "status": "ZERO_EARNINGS"
    }


def test_invalid_pets_both_zero_and_negative():
    routes = [route(walks=[{"num_pets": 0}, {"num_pets": -2}, {"num_pets": 2}])]
    assert process_walking_routes(routes, 5)["total_revenue"] == 32.0


def test_pet_count_boundary_regular_and_group_discount():
    # 3 pets: 22 + 3*5; 4 pets: (22 + 4*8)*0.90
    routes = [route(walks=[{"num_pets": 3}, {"num_pets": 4}])]
    assert process_walking_routes(routes, 5)["total_revenue"] == 85.6


def test_medication_fee_applies_only_if_requested():
    routes = [route(walks=[{"num_pets": 1, "needs_meds": False},
                                 {"num_pets": 1, "needs_meds": True}])]
    assert process_walking_routes(routes, 5)["total_revenue"] == 60.0


def test_standard_60_aggression_resets_fee_and_breaks():
    routes = [route("standard_60", [{"num_pets": 2},
                                   {"num_pets": 1, "aggression_alert": True},
                                   {"num_pets": 5}])]
    assert process_walking_routes(routes, 5)["status"] == "ZERO_EARNINGS"


def test_non_60_aggression_counts_incident_but_walks_continue():
    routes = [route("express_15", [{"num_pets": 1, "aggression_alert": True, "needs_meds": True},
                                    {"num_pets": 2}])]
    assert process_walking_routes(routes, 5) == {"total_revenue": 30.0, "status": "COMPLETED"}


def test_weekend_transport_fee_vs_weekday():
    walk = [{"num_pets": 1}]
    assert process_walking_routes([route(walks=walk, weekend=False)], 5)["total_revenue"] == 27.0
    assert process_walking_routes([route(walks=walk, weekend=True)], 5)["total_revenue"] == 32.0


def test_no_walks_but_weekend_transport_is_charged():
    assert process_walking_routes([route(walks=[], weekend=True)], 7) == {
        "total_revenue": 7.0, "status": "COMPLETED"
    }


def test_four_incidents_does_not_trigger_audit_but_five_does():
    for incidents, expected_status in [(4, "ZERO_EARNINGS"), (5, "INCIDENT_AUDIT")]:
        result = process_walking_routes([route(walks=[{"num_pets": 0}] * incidents)], 0)
        assert result["status"] == expected_status


def test_multiple_routes_and_successful_total():
    routes = [route("standard_30", [{"num_pets": 1}]),
              route("express_15", [{"num_pets": 1}], weekend=True),
              route("bad_session", [{"num_pets": 1}]),
              route(confirmed=False)]
    assert process_walking_routes(routes, 5) == {"total_revenue": 51.0, "status": "COMPLETED"}


def test_gps_no_data_for_empty_outer_list():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_online_for_empty_inner_and_good_readings():
    assert inspect_gps_collars([[], [20, 50, 100]]) == "ONLINE"


def test_gps_streak_resets_on_strong_signal_and_new_collar():
    assert inspect_gps_collars([[19, 20, 19], [19, 20]]) == "ONLINE"


def test_gps_signal_just_below_threshold_two_in_row():
    assert inspect_gps_collars([[20, 19, 19]]) == "LOST_SIGNAL_ALERT"


def test_gps_lost_on_later_collar():
    assert inspect_gps_collars([[40, 19, 40], [100, 19, 1]]) == "LOST_SIGNAL_ALERT"
