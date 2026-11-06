// Backfills ticket codes for existing reservations that have null or empty ticket codes.
function "Quick Start/backfill_ticket_codes" {
  input {
  }

  stack {
    db.query reservation {
      return = {type: "list"}
    } as $reservations

    var $updated_count {
      value = 0
    }

    foreach ($reservations) {
      each as $res {
        conditional {
          if ($res.ticket_code == null || $res.ticket_code == "") {
            function.run "Quick Start/generate_ticket_code" {} as $ticket_result

            db.edit reservation {
              field_name = "id"
              field_value = $res.id
              data = {ticket_code: $ticket_result.ticket_code}
            } as $updated_res

            var.update $updated_count {
              value = $updated_count + 1
            }
          }
        }
      }
    }
  }

  response = {updated_count: $updated_count}
  tags = ["xano:quick-start", "ticket-management"]
  guid = "backfill-ticket-codes-guid-001"
}
