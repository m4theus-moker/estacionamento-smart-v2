query reservation verb=POST {
  api_group = "Parking Management"
  auth = "user"

  input {
    int location_id
    int vaga_id
    int vehicle_id
    timestamp start_time
    timestamp end_time
  }

  stack {
    precondition ($input.start_time >= () now) {
      error_type = "inputerror"
      error = "A data/hora de início não pode ser no passado."
    }
  
    precondition ($input.end_time > $input.start_time) {
      error_type = "inputerror"
      error = "A data/hora de término deve ser posterior à de início."
    }
  
    db.get vehicle {
      field_name = "id"
      field_value = $input.vehicle_id
    } as $vehicle
  
    precondition ($vehicle != null && $vehicle.user_id == $auth.id) {
      error_type = "inputerror"
      error = "Veículo inválido ou não pertence ao usuário."
    }
  
    db.get vaga {
      field_name = "id"
      field_value = $input.vaga_id
    } as $vaga
  
    precondition ($vaga != null && $vaga.location_id == $input.location_id) {
      error_type = "inputerror"
      error = "Vaga inválida ou não pertence ao local informado."
    }
  
    precondition ((($vehicle.type == null || $vehicle.type == "" || $vehicle.type == "carro") && ($vaga.tipo == "carro" || $vaga.tipo == "eletrico")) || ($vehicle.type == "moto" && $vaga.tipo == "moto") || ($vehicle.type == "pcd" && ($vaga.tipo == "pcd" || $vaga.tipo == "carro")) || ($vehicle.type == "eletrico" && ($vaga.tipo == "eletrico" || $vaga.tipo == "carro"))) {
      error_type = "inputerror"
      error = "Incompatibilidade: O tipo do veículo não é compatível com o tipo da vaga selecionada."
    }
  
    db.query tarifa {
      where = $db.tarifa.location_id == $input.location_id && $db.tarifa.tipo_vaga == $vaga.tipo
      return = {type: "single"}
    } as $tarifa
  
    precondition ($tarifa != null) {
      error_type = "inputerror"
      error = "Tarifa não cadastrada para este tipo de vaga no local."
    }
  
    db.query reservation {
      where = $db.reservation.vaga_id == $input.vaga_id && $db.reservation.status == "ativa" && $db.reservation.start_time < $input.end_time && $db.reservation.end_time > $input.start_time
      return = {type: "single"}
    } as $conflict
  
    precondition ($conflict == null) {
      error_type = "inputerror"
      error = "Conflito de horário: Vaga já reservada neste período."
    }
  
    var $cursor {
      value = $input.start_time
    }
  
    var $horas {
      value = 0
    }
  
    while ($cursor < $input.end_time) {
      each {
        var.update $cursor {
          value = $cursor|add_secs_to_timestamp:3600
        }
      
        var.update $horas {
          value = $horas + 1
        }
      }
    }
  
    conditional {
      if ($horas < 1) {
        var.update $horas {
          value = 1
        }
      }
    }
  
    var $total_price {
      value = $horas * $tarifa.valor_hora
    }
  
    function.run "Quick Start/generate_ticket_code" {} as $ticket_result
  
    db.add reservation {
      data = {
        created_at : "now"
        user_id    : $auth.id
        location_id: $input.location_id
        vaga_id    : $input.vaga_id
        vehicle_id : $input.vehicle_id
        start_time : $input.start_time
        end_time   : $input.end_time
        status     : "ativa"
        price      : $total_price
        ticket_code: $ticket_result.ticket_code
      }
    } as $reservation
  }

  response = $reservation
  tags = ["reservation-management"]
  guid = "reservation-post-guid-001"
}