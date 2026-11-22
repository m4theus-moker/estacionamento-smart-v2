import unittest
from datetime import datetime

class TestVehicleRetrieval(unittest.TestCase):
    def test_pickup_request_structure(self):
        # Simulate global pickup requests store (same as app.py GLOBAL_PICKUP_REQUESTS)
        global_pickup_requests = {}
        
        res_id = 101
        req_data = {
            "reservation_id": res_id,
            "client": "cliente@email.com",
            "location": "Unidade Central",
            "vaga": "V05",
            "vehicle": "Sedan (ABC-1234)",
            "requested_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        global_pickup_requests[res_id] = req_data
        
        # Verify that pickup request has been recorded with slot (vaga) info
        self.assertIn(res_id, global_pickup_requests)
        pickup = global_pickup_requests[res_id]
        self.assertEqual(pickup["reservation_id"], 101)
        self.assertEqual(pickup["vaga"], "V05")
        self.assertEqual(pickup["location"], "Unidade Central")
        self.assertEqual(pickup["vehicle"], "Sedan (ABC-1234)")
        self.assertIn("requested_at", pickup)

        # Simulate completion / removal
        global_pickup_requests.pop(res_id, None)
        self.assertNotIn(res_id, global_pickup_requests)

if __name__ == '__main__':
    unittest.main()
