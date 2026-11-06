import unittest
import html
from datetime import datetime

def generate_ticket_html(ticket_code, client_name, vehicle_plate, location_name, vaga_numero, start_time, end_time, price, status, issued_at):
    safe_client = html.escape(str(client_name))
    safe_plate = html.escape(str(vehicle_plate))
    safe_location = html.escape(str(location_name))
    safe_vaga = html.escape(str(vaga_numero))
    safe_status = html.escape(str(status))
    safe_code = html.escape(str(ticket_code))
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Ticket de Reserva - {safe_code}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #111; }}
        .ticket {{ border: 2px dashed #22c55e; padding: 20px; border-radius: 8px; max-width: 600px; margin: auto; background: #f9fafb; }}
        .header {{ text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 20px; }}
        .code {{ font-size: 24px; font-weight: bold; color: #22c55e; font-family: monospace; }}
        .details {{ margin-bottom: 15px; }}
        .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }}
        @media print {{
            body {{ margin: 0; }}
            .ticket {{ border: 2px solid #000; box-shadow: none; width: 100%; max-width: none; }}
        }}
    </style>
</head>
<body>
    <div class="ticket">
        <div class="header">
            <h2>Estacionamento Smart - Ticket de Reserva</h2>
            <div class="code">{safe_code}</div>
        </div>
        <div class="details">
            <p><strong>Cliente:</strong> {safe_client}</p>
            <p><strong>Veículo (Placa):</strong> {safe_plate}</p>
            <p><strong>Local:</strong> {safe_location}</p>
            <p><strong>Vaga:</strong> {safe_vaga}</p>
            <p><strong>Início:</strong> {start_time}</p>
            <p><strong>Término:</strong> {end_time}</p>
            <p><strong>Preço Total:</strong> R$ {price:.2f}</p>
            <p><strong>Status:</strong> {safe_status}</p>
        </div>
        <div class="footer">
            <p>Emitido em: {issued_at}</p>
        </div>
    </div>
</body>
</html>"""
    return html_content

class TestTicketGeneration(unittest.TestCase):
    def test_ticket_html_escaping_and_emitido_em(self):
        malicious_client = '<script>alert("XSS")</script>João'
        malicious_plate = '<b>ABC-1234</b>'
        ticket_code = 'ABC2DEF7'
        location_name = 'Central Park'
        vaga_numero = 'V01'
        start_time = '04/11/2026 10:00'
        end_time = '04/11/2026 12:00'
        price = 20.00
        status = 'Válido'
        issued_at = '04/11/2026 09:30'

        html_output = generate_ticket_html(
            ticket_code=ticket_code,
            client_name=malicious_client,
            vehicle_plate=malicious_plate,
            location_name=location_name,
            vaga_numero=vaga_numero,
            start_time=start_time,
            end_time=end_time,
            price=price,
            status=status,
            issued_at=issued_at
        )

        # Verify HTML escaping
        self.assertNotIn('<script>alert("XSS")</script>', html_output)
        self.assertIn('&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;João', html_output)
        self.assertNotIn('<b>ABC-1234</b>', html_output)
        self.assertIn('&lt;b&gt;ABC-1234&lt;/b&gt;', html_output)

        # Verify "Emitido em"
        self.assertIn('Emitido em: 04/11/2026 09:30', html_output)
        self.assertIn('ABC2DEF7', html_output)

if __name__ == '__main__':
    unittest.main()
