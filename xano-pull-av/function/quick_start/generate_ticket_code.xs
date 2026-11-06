// UUID hex maiúsculo com 0->G e 1->H; todos os caracteres pertencem ao alfabeto ABCDEFGHJKMNPQRSTUVWXYZ23456789
function "Quick Start/generate_ticket_code" {
  input {}

  stack {
    var $success {
      value = false
    }
  
    var $ticket_code {
      value = ""
    }
  
    var $attempts {
      value = 0
    }
  
    while ($attempts < 5 && $success == false) {
      each {
        var.update $attempts {
          value = $attempts + 1
        }
      
        security.create_uuid as $uuid
      
        var $clean {
          value = $uuid|to_upper|replace:"0":"G"|replace:"1":"H"
        }
      
        var $code {
          value = $clean|substr:0:8
        }
      
        db.query reservation {
          where = $db.reservation.ticket_code == $code
          return = {type: "single"}
        } as $existing
      
        conditional {
          if ($existing == null) {
            var.update $ticket_code {
              value = $code
            }
            var.update $success {
              value = true
            }
          }
        }
      }
    }
  
    precondition ($success == true) {
      error_type = "inputerror"
      error = "Falha ao gerar código de ticket único após 5 tentativas."
    }
  }

  response = {ticket_code: $ticket_code}
  tags = ["xano:quick-start", "ticket-management"]
  guid = "a9Aa_DwkeX_4bZY_eIxEKMOhhPA"
}
