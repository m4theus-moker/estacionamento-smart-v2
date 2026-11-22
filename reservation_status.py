from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

def parse_timestamp_to_datetime(ts):
    if not ts:
        return None
    if isinstance(ts, datetime):
        tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
        if tz and ts.tzinfo is None:
            return ts.replace(tzinfo=tz)
        elif tz:
            return ts.astimezone(tz)
        return ts
    try:
        val = float(ts)
        if val > 1e11:
            val = val / 1000.0
        if ZoneInfo:
            try:
                return datetime.fromtimestamp(val, tz=ZoneInfo("America/Sao_Paulo"))
            except Exception:
                pass
        return datetime.fromtimestamp(val)
    except Exception:
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else None
                if tz and dt.tzinfo is None:
                    dt = dt.replace(tzinfo=tz)
                elif tz:
                    dt = dt.astimezone(tz)
                return dt
            except Exception:
                pass
        return None

def calculate_reservation_status(raw_status, start_ts, end_ts):
    if raw_status and str(raw_status).strip().lower() in ["cancelada", "cancelado"]:
        return "Cancelado"
    
    start_dt = parse_timestamp_to_datetime(start_ts)
    end_dt = parse_timestamp_to_datetime(end_ts)
    
    if ZoneInfo:
        try:
            agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        except Exception:
            agora = datetime.now()
    else:
        agora = datetime.now()
        
    if not start_dt or not end_dt:
        s = str(raw_status or "válido").strip().capitalize()
        return s if s in ["Válido", "Em andamento", "Expirado", "Cancelado"] else "Válido"
        
    if agora < start_dt:
        return "Válido"
    elif start_dt <= agora < end_dt:
        return "Em andamento"
    else:
        return "Expirado"
