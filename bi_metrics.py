import pandas as pd
from datetime import datetime, timedelta
from reservation_status import calculate_reservation_status
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

def parse_datetime(val):
    if val is None:
        return None
    tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
    
    if isinstance(val, (int, float)):
        sec = val / 1000.0 if val > 1e11 else val
        dt = datetime.fromtimestamp(sec)
        if tz:
            dt = dt.astimezone(tz)
        return dt
    elif isinstance(val, str):
        try:
            dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
            if tz and dt.tzinfo is None:
                dt = dt.replace(tzinfo=tz)
            elif tz:
                dt = dt.astimezone(tz)
            return dt
        except Exception:
            return None
    elif isinstance(val, datetime):
        if tz and val.tzinfo is None:
            return val.replace(tzinfo=tz)
        elif tz:
            return val.astimezone(tz)
        return val
    return None

def filter_valid_reservations(reservations):
    if not reservations:
        return []
    valid = []
    for r in reservations:
        if not isinstance(r, dict):
            continue
        status = str(r.get('status', 'ativa')).strip().lower()
        if status in ['cancelada', 'cancelado']:
            continue
        valid.append(r)
    return valid

def filter_reservations_by_date_range(reservations, period_type="all", custom_start=None, custom_end=None, now=None):
    if not reservations:
        return []
    
    if not now:
        tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
        now = datetime.now(tz) if tz else datetime.now()
    else:
        now = parse_datetime(now) or now
    today = now.date()

    filtered = []
    for r in reservations:
        if not isinstance(r, dict):
            continue
        start_dt = parse_datetime(r.get('start_time'))
        if not start_dt:
            continue
        r_date = start_dt.date()

        if period_type == "hoje":
            if r_date == today:
                filtered.append(r)
        elif period_type == "ultimos_7_dias":
            if today - timedelta(days=6) <= r_date <= today:
                filtered.append(r)
        elif period_type == "este_mes":
            if r_date.year == today.year and r_date.month == today.month:
                filtered.append(r)
        elif period_type == "personalizado":
            if custom_start and custom_end:
                if custom_start <= r_date <= custom_end:
                    filtered.append(r)
            else:
                filtered.append(r)
        else: # "all"
            filtered.append(r)
    return filtered

def calculate_status_distribution(reservations):
    if not reservations:
        return {"Válido": 0, "Em andamento": 0, "Expirado": 0, "Cancelado": 0}
    dist = {"Válido": 0, "Em andamento": 0, "Expirado": 0, "Cancelado": 0}
    for r in reservations:
        if not isinstance(r, dict):
            continue
        calc_status = calculate_reservation_status(r.get('status'), r.get('start_time'), r.get('end_time'))
        if calc_status in dist:
            dist[calc_status] += 1
        else:
            dist["Válido"] += 1
    return dist

def calculate_daily_revenue_trend(reservations):
    valid = filter_valid_reservations(reservations)
    daily_map = {}
    for r in valid:
        start_dt = parse_datetime(r.get('start_time'))
        price = float(r.get('price') or 0.0)
        if not start_dt:
            continue
        date_str = start_dt.strftime("%Y-%m-%d")
        daily_map[date_str] = daily_map.get(date_str, 0.0) + price
    
    sorted_dates = sorted(daily_map.keys())
    return {d: daily_map[d] for d in sorted_dates}

def calculate_category_metrics(reservations, slots):
    valid = filter_valid_reservations(reservations)
    slot_type_map = {}
    if slots:
        for s in slots:
            if isinstance(s, dict):
                t = s.get('type') or s.get('tipo') or 'comum'
                slot_type_map[s.get('id')] = str(t).strip().lower()

    cat_revenue = {}
    cat_count = {}
    for r in valid:
        vaga_id = r.get('vaga_id')
        ctype = slot_type_map.get(vaga_id, 'comum')
        price = float(r.get('price') or 0.0)
        
        cat_revenue[ctype] = cat_revenue.get(ctype, 0.0) + price
        cat_count[ctype] = cat_count.get(ctype, 0) + 1

    return {
        "revenue_by_category": cat_revenue,
        "count_by_category": cat_count
    }

def calculate_weekday_revenue(reservations):
    valid = filter_valid_reservations(reservations)
    weekdays = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    weekday_rev = {w: 0.0 for w in weekdays}
    
    for r in valid:
        start_dt = parse_datetime(r.get('start_time'))
        price = float(r.get('price') or 0.0)
        if not start_dt:
            continue
        wd_idx = start_dt.weekday()
        w_name = weekdays[wd_idx]
        weekday_rev[w_name] += price
        
    return weekday_rev

def calculate_revenue_metrics(reservations, now=None):
    valid = filter_valid_reservations(reservations)
    if not now:
        tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
        now = datetime.now(tz) if tz else datetime.now()
    else:
        now = parse_datetime(now) or now

    daily_rev = 0.0
    weekly_rev = 0.0
    monthly_rev = 0.0

    today_date = now.date()
    start_of_week = today_date - timedelta(days=today_date.weekday())
    current_month = today_date.month
    current_year = today_date.year

    for r in valid:
        start_dt = parse_datetime(r.get('start_time'))
        price = float(r.get('price') or 0.0)
        if not start_dt:
            continue
        if start_dt > now:
            continue
        r_date = start_dt.date()

        if r_date == today_date:
            daily_rev += price
        if r_date >= start_of_week and r_date <= today_date:
            weekly_rev += price
        if r_date.month == current_month and r_date.year == current_year and r_date <= today_date:
            monthly_rev += price

    elapsed_days = max(today_date.day, 1)
    if current_month == 12:
        next_month = datetime(current_year + 1, 1, 1)
    else:
        next_month = datetime(current_year, current_month + 1, 1)
    total_days_in_month = (next_month - datetime(current_year, current_month, 1)).days

    projected_monthly = (monthly_rev / elapsed_days) * total_days_in_month if elapsed_days > 0 else 0.0

    return {
        "daily": daily_rev,
        "weekly": weekly_rev,
        "monthly": monthly_rev,
        "projected_monthly": projected_monthly
    }

def calculate_occupancy_metric(reservations, total_slots, now=None):
    valid = filter_valid_reservations(reservations)
    if not now:
        tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
        now = datetime.now(tz) if tz else datetime.now()
    else:
        now = parse_datetime(now) or now

    active_count = 0
    for r in valid:
        status = str(r.get('status', 'ativa')).strip().lower()
        if status != 'ativa':
            continue
        start_dt = parse_datetime(r.get('start_time'))
        end_dt = parse_datetime(r.get('end_time'))
        if start_dt and end_dt:
            if start_dt <= now < end_dt:
                active_count += 1

    total = max(int(total_slots or 0), 1)
    occupancy_rate = min(float(active_count) / float(total), 1.0)

    return {
        "active_count": active_count,
        "total_slots": total,
        "occupancy_rate": occupancy_rate
    }

def calculate_ticket_and_duration(reservations):
    valid = filter_valid_reservations(reservations)
    if not valid:
        return {"avg_ticket": 0.0, "avg_duration_hours": 0.0}

    total_price = 0.0
    total_duration_secs = 0.0
    count_ticket = 0
    count_duration = 0

    for r in valid:
        price = r.get('price')
        if price is not None:
            try:
                total_price += float(price)
                count_ticket += 1
            except Exception:
                pass

        start_dt = parse_datetime(r.get('start_time'))
        end_dt = parse_datetime(r.get('end_time'))
        if start_dt and end_dt:
            diff = (end_dt - start_dt).total_seconds()
            if diff > 0:
                total_duration_secs += diff
                count_duration += 1

    avg_ticket = (total_price / count_ticket) if count_ticket > 0 else 0.0
    avg_duration_hours = (total_duration_secs / count_duration / 3600.0) if count_duration > 0 else 0.0

    return {
        "avg_ticket": avg_ticket,
        "avg_duration_hours": avg_duration_hours
    }

def calculate_turnover(reservations, slots):
    valid = filter_valid_reservations(reservations)
    slot_counts = {}
    for r in valid:
        vaga_id = r.get('vaga_id')
        if vaga_id:
            slot_counts[vaga_id] = slot_counts.get(vaga_id, 0) + 1

    total_slots = max(len(slots) if slots else 1, 1)
    total_reservations = len(valid)
    lot_turnover = float(total_reservations) / float(total_slots)

    return {
        "slot_turnover": slot_counts,
        "lot_turnover": lot_turnover
    }

def calculate_peak_hours(reservations):
    valid = filter_valid_reservations(reservations)
    hours = [0] * 24
    for r in valid:
        start_dt = parse_datetime(r.get('start_time'))
        end_dt = parse_datetime(r.get('end_time'))
        if not start_dt:
            continue
        if not end_dt:
            end_dt = start_dt + timedelta(hours=1)
        if end_dt <= start_dt:
            end_dt = start_dt + timedelta(hours=1)
            
        for h in range(24):
            d = start_dt.date()
            end_date = end_dt.date()
            covered = False
            while d <= end_date:
                try:
                    h_start = datetime.combine(d, datetime.min.time()).replace(hour=h, tzinfo=start_dt.tzinfo if hasattr(start_dt, 'tzinfo') else None)
                    h_end = h_start + timedelta(hours=1)
                except Exception:
                    h_start = datetime(d.year, d.month, d.day, h, 0)
                    h_end = h_start + timedelta(hours=1)
                
                if start_dt < h_end and end_dt > h_start:
                    covered = True
                    break
                d += timedelta(days=1)
            if covered:
                hours[h] += 1
    return hours
