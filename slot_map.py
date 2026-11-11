def classify_slot(slot, free_slot_ids, user_reservations, query_start, query_end):
    """
    Pure function to classify a parking slot state:
    - 'Livre': slot is in free_slot_ids (returned by availability endpoint).
    - 'Sua reserva': slot belongs to an active overlapping reservation of the user
      (start_res < query_end and end_res > query_start and status != 'cancelada').
    - 'Indisponível': otherwise (occupied by another reservation or incompatible with vehicle type).
    """
    slot_id = slot.get('id')
    
    # Check if user has an active overlapping reservation on this slot
    for res in user_reservations:
        if res.get('vaga_id') == slot_id:
            res_status = str(res.get('status', 'ativa')).strip().lower()
            if res_status not in ['cancelada', 'cancelado']:
                r_start = res.get('start_time')
                r_end = res.get('end_time')
                # Overlap condition: start_res < query_end and end_res > query_start
                if r_start and r_end and r_start < query_end and r_end > query_start:
                    return 'Sua reserva'

    # Check if free
    if slot_id in free_slot_ids:
        return 'Livre'

    return 'Indisponível'
