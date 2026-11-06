query "reservation/{id}/ticket" verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get reservation {
      field_name = "id"
      field_value = $input.id
    } as $reservation
  
    precondition ($reservation != null && $reservation.user_id == $auth.id) {
      error_type = "notfound"
      error = "Reserva não encontrada."
    }
  
    db.get location {
      field_name = "id"
      field_value = $reservation.location_id
      output = ["name"]
    } as $location
  
    db.get vaga {
      field_name = "id"
      field_value = $reservation.vaga_id
      output = ["numero", "tipo"]
    } as $vaga
  
    db.get vehicle {
      field_name = "id"
      field_value = $reservation.vehicle_id
      output = ["plate", "brand", "model", "type"]
    } as $vehicle
  
    var $loc_name {
      value = null
    }
    conditional {
      if ($location != null) {
        var.update $loc_name {
          value = $location.name
        }
      }
    }

    var $vaga_num {
      value = null
    }
    var $vaga_t {
      value = null
    }
    conditional {
      if ($vaga != null) {
        var.update $vaga_num {
          value = $vaga.numero
        }
        var.update $vaga_t {
          value = $vaga.tipo
        }
      }
    }

    var $veh_plate {
      value = null
    }
    var $veh_brand {
      value = null
    }
    var $veh_model {
      value = null
    }
    var $veh_type {
      value = null
    }
    conditional {
      if ($vehicle != null) {
        var.update $veh_plate {
          value = $vehicle.plate
        }
        var.update $veh_brand {
          value = $vehicle.brand
        }
        var.update $veh_model {
          value = $vehicle.model
        }
        var.update $veh_type {
          value = $vehicle.type
        }
      }
    }

    var $ticket_status {
      value = "Válido"
    }
  
    conditional {
      if ($reservation.status == "cancelada") {
        var.update $ticket_status {
          value = "Cancelado"
        }
      }
    }
  
    conditional {
      if ($reservation.status == "concluida" || ($reservation.status == "ativa" && () now >= $reservation.end_time)) {
        var.update $ticket_status {
          value = "Expirado"
        }
      }
    }
  
    conditional {
      if ($reservation.status == "ativa" && $reservation.start_time <= () now && () now < $reservation.end_time) {
        var.update $ticket_status {
          value = "Em andamento"
        }
      }
    }
  }

  response = {
    ticket_code: $reservation.ticket_code
    status: $ticket_status
    start_time: $reservation.start_time
    end_time: $reservation.end_time
    price: $reservation.price
    location_name: $loc_name
    vaga_numero: $vaga_num
    vaga_tipo: $vaga_t
    vehicle_plate: $veh_plate
    vehicle_brand: $veh_brand
    vehicle_model: $veh_model
    vehicle_type: $veh_type
  }

  tags = ["reservation-management"]
  guid = "reservation-ticket-guid-001"
}
