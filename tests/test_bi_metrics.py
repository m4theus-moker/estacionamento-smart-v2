import pytest
from datetime import datetime, timedelta
from bi_metrics import (
    parse_datetime,
    filter_valid_reservations,
    filter_reservations_by_date_range,
    calculate_status_distribution,
    calculate_daily_revenue_trend,
    calculate_category_metrics,
    calculate_weekday_revenue,
    calculate_revenue_metrics,
    calculate_occupancy_metric,
    calculate_ticket_and_duration,
    calculate_turnover,
    calculate_peak_hours
)

def test_parse_datetime():
    dt_str = "2026-11-11T10:00:00"
    parsed = parse_datetime(dt_str)
    assert parsed is not None
    assert parsed.year == 2026

    # Timestamp in milliseconds
    ts_ms = 1778680800000 # ~2026
    parsed_ts = parse_datetime(ts_ms)
    assert parsed_ts is not None

    assert parse_datetime(None) is None
    assert parse_datetime("invalid-date") is None

def test_filter_valid_reservations():
    res = [
        {"id": 1, "status": "ativa", "price": 50},
        {"id": 2, "status": "cancelada", "price": 30},
        {"id": 3, "status": "CONCLUIDA", "price": 40},
        "not-a-dict"
    ]
    valid = filter_valid_reservations(res)
    assert len(valid) == 2
    assert valid[0]["id"] == 1
    assert valid[1]["id"] == 3

def test_filter_reservations_by_date_range():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"id": 1, "start_time": now.isoformat()},
        {"id": 2, "start_time": (now - timedelta(days=10)).isoformat()}
    ]
    filtered_today = filter_reservations_by_date_range(res, period_type="hoje", now=now)
    assert len(filtered_today) == 1
    assert filtered_today[0]["id"] == 1

    filtered_all = filter_reservations_by_date_range(res, period_type="all", now=now)
    assert len(filtered_all) == 2

def test_calculate_status_distribution():
    now = datetime.now()
    future_start = (now + timedelta(days=1)).isoformat()
    future_end = (now + timedelta(days=2)).isoformat()
    past_start = (now - timedelta(days=2)).isoformat()
    past_end = (now - timedelta(days=1)).isoformat()

    res = [
        {"status": "ativa", "start_time": future_start, "end_time": future_end},
        {"status": "cancelada", "start_time": future_start, "end_time": future_end},
        {"status": "ativa", "start_time": past_start, "end_time": past_end}
    ]
    dist = calculate_status_distribution(res)
    assert dist["Válido"] == 1
    assert dist["Cancelado"] == 1
    assert dist["Expirado"] == 1

def test_calculate_daily_revenue_trend():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"start_time": now.isoformat(), "price": 50.0, "status": "ativa"},
        {"start_time": now.isoformat(), "price": 25.0, "status": "concluida"}
    ]
    trend = calculate_daily_revenue_trend(res)
    assert "2026-11-11" in trend
    assert trend["2026-11-11"] == 75.0

def test_calculate_category_metrics():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"vaga_id": 1, "price": 40.0, "status": "ativa", "start_time": now.isoformat()},
        {"vaga_id": 2, "price": 60.0, "status": "concluida", "start_time": now.isoformat()}
    ]
    slots = [
        {"id": 1, "type": "comum"},
        {"id": 2, "type": "eletrico"}
    ]
    metrics = calculate_category_metrics(res, slots)
    assert metrics["revenue_by_category"]["comum"] == 40.0
    assert metrics["revenue_by_category"]["eletrico"] == 60.0
    assert metrics["count_by_category"]["comum"] == 1

def test_calculate_weekday_revenue():
    now = datetime(2026, 11, 11, 12, 0, 0) # 2026-11-11 is a Wednesday (Quarta)
    res = [
        {"start_time": now.isoformat(), "price": 100.0, "status": "ativa"}
    ]
    wd_rev = calculate_weekday_revenue(res)
    assert wd_rev["Quarta"] == 100.0
    assert wd_rev["Segunda"] == 0.0

def test_calculate_revenue_metrics():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"start_time": now.isoformat(), "price": 20.0, "status": "ativa"},
        {"start_time": (now - timedelta(days=1)).isoformat(), "price": 30.0, "status": "concluida"},
        {"start_time": now.isoformat(), "price": 100.0, "status": "cancelada"}
    ]
    metrics = calculate_revenue_metrics(res, now=now)
    assert metrics["daily"] == 20.0
    assert metrics["monthly"] == 50.0
    assert metrics["projected_monthly"] > 0

def test_calculate_occupancy_metric():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {
            "start_time": (now - timedelta(hours=1)).isoformat(),
            "end_time": (now + timedelta(hours=1)).isoformat(),
            "status": "ativa",
            "vaga_id": 1
        },
        {
            "start_time": (now + timedelta(hours=2)).isoformat(),
            "end_time": (now + timedelta(hours=3)).isoformat(),
            "status": "ativa",
            "vaga_id": 2
        }
    ]
    occ = calculate_occupancy_metric(res, total_slots=4, now=now)
    assert occ["active_count"] == 1
    assert occ["total_slots"] == 4
    assert occ["occupancy_rate"] == 0.25

def test_calculate_ticket_and_duration():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(hours=2)).isoformat(),
            "price": 40.0,
            "status": "ativa"
        },
        {
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(hours=4)).isoformat(),
            "price": 80.0,
            "status": "concluida"
        }
    ]
    metrics = calculate_ticket_and_duration(res)
    assert metrics["avg_ticket"] == 60.0
    assert metrics["avg_duration_hours"] == 3.0

def test_calculate_turnover():
    res = [
        {"vaga_id": 1, "status": "ativa"},
        {"vaga_id": 1, "status": "concluida"},
        {"vaga_id": 2, "status": "ativa"}
    ]
    slots = [{"id": 1}, {"id": 2}, {"id": 3}]
    turn = calculate_turnover(res, slots)
    assert turn["slot_turnover"][1] == 2
    assert turn["slot_turnover"][2] == 1
    assert turn["lot_turnover"] == 1.0

def test_calculate_peak_hours():
    dt = datetime(2026, 11, 11, 14, 30, 0)
    res = [{"start_time": dt.isoformat(), "status": "ativa"}]
    hours = calculate_peak_hours(res)
    assert hours[14] == 1
    assert hours[0] == 0

def test_calculate_revenue_metrics_excludes_future_and_cancelled():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"start_time": datetime(2026, 11, 10, 10, 0, 0).isoformat(), "price": 50.0, "status": "ativa"},
        {"start_time": datetime(2026, 11, 15, 10, 0, 0).isoformat(), "price": 100.0, "status": "ativa"},
        {"start_time": datetime(2026, 11, 5, 10, 0, 0).isoformat(), "price": 200.0, "status": "cancelada"}
    ]
    metrics = calculate_revenue_metrics(res, now=now)
    assert metrics["monthly"] == 50.0

def test_calculate_revenue_metrics_projection():
    now = datetime(2026, 11, 11, 12, 0, 0)
    res = [
        {"start_time": datetime(2026, 11, 1, 10, 0, 0).isoformat(), "price": 110.0, "status": "ativa"}
    ]
    metrics = calculate_revenue_metrics(res, now=now)
    assert metrics["monthly"] == 110.0
    assert metrics["projected_monthly"] == 300.0

def test_period_filter_does_not_alter_month_kpi():
    now = datetime(2026, 11, 11, 12, 0, 0)
    all_res = [
        {"start_time": datetime(2026, 11, 1, 10, 0, 0).isoformat(), "price": 50.0, "status": "ativa"},
        {"start_time": datetime(2026, 11, 11, 10, 0, 0).isoformat(), "price": 30.0, "status": "ativa"}
    ]
    filtered_res = filter_reservations_by_date_range(all_res, period_type="hoje", now=now)
    assert len(filtered_res) == 1
    metrics = calculate_revenue_metrics(all_res, now=now)
    assert metrics["monthly"] == 80.0
