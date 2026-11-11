import pytest
from slot_map import classify_slot

def test_classify_slot_livre():
    slot = {'id': 1, 'numero': 'V01', 'tipo': 'carro'}
    free_slot_ids = [1, 2]
    user_reservations = []
    state = classify_slot(slot, free_slot_ids, user_reservations, '2026-11-10T10:00', '2026-11-10T12:00')
    assert state == 'Livre'

def test_classify_slot_indisponivel():
    slot = {'id': 3, 'numero': 'V03', 'tipo': 'moto'}
    free_slot_ids = [1, 2]
    user_reservations = []
    state = classify_slot(slot, free_slot_ids, user_reservations, '2026-11-10T10:00', '2026-11-10T12:00')
    assert state == 'Indisponível'

def test_classify_slot_sua_reserva():
    slot = {'id': 4, 'numero': 'V04', 'tipo': 'carro'}
    free_slot_ids = [1, 2]
    user_reservations = [
        {
            'id': 10,
            'vaga_id': 4,
            'start_time': '2026-11-10T09:00',
            'end_time': '2026-11-10T11:00',
            'status': 'ativa'
        }
    ]
    state = classify_slot(slot, free_slot_ids, user_reservations, '2026-11-10T10:00', '2026-11-10T12:00')
    assert state == 'Sua reserva'

def test_classify_slot_reserva_cancelada_ignornada():
    slot = {'id': 4, 'numero': 'V04', 'tipo': 'carro'}
    free_slot_ids = [1, 2]
    user_reservations = [
        {
            'id': 10,
            'vaga_id': 4,
            'start_time': '2026-11-10T09:00',
            'end_time': '2026-11-10T11:00',
            'status': 'cancelada'
        }
    ]
    state = classify_slot(slot, free_slot_ids, user_reservations, '2026-11-10T10:00', '2026-11-10T12:00')
    assert state == 'Indisponível'
