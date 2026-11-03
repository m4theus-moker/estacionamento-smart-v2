query "reservation/availability" verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int location_id
    int vehicle_id
    timestamp start_time
    timestamp end_time
  }

  stack {
    db.get vehicle {
      field_name = "id"
      field_value = $input.vehicle_id
    } as $vehicle
  
    precondition ($vehicle != null && $vehicle.user_id == $auth.id) {
      error_type = "inputerror"
      error = "Veículo inválido ou não pertence ao usuário."
    }
  
    precondition ($vehicle.type != null && $vehicle.type != "") {
      error_type = "inputerror"
      error = "Informe o tipo do veículo em Meus Veículos."
    }
  
    precondition ($input.start_time < $input.end_time) {
      error_type = "inputerror"
      error = "A data/hora de término deve ser posterior à de início."
    }
  
    db.query vaga {
      where = $db.vaga.location_id == $input.location_id && (($vehicle.type == "carro" && ($db.vaga.tipo == "carro" || $db.vaga.tipo == "eletrico")) || ($vehicle.type == "moto" && $db.vaga.tipo == "moto") || ($vehicle.type == "pcd" && ($db.vaga.tipo == "pcd" || $db.vaga.tipo == "carro")))
      return = {type: "list"}
    } as $vagas
  
    db.query reservation {
      where = $db.reservation.location_id == $input.location_id && $db.reservation.status == "ativa" && $db.reservation.start_time < $input.end_time && $db.reservation.end_time > $input.start_time
      return = {type: "list"}
    } as $active_reservations
  
    var $livres {
      value = []
    }
  
    foreach ($vagas) {
      each as $vaga_item {
        var $ocupada {
          value = false
        }
      
        foreach ($active_reservations) {
          each as $res_item {
            conditional {
              if ($res_item.vaga_id == $vaga_item.id) {
                var.update $ocupada {
                  value = true
                }
              }
            }
          }
        }
      
        conditional {
          if ($ocupada == false) {
            array.push $livres {
              value = $vaga_item
            }
          }
        }
      }
    }
  }

  response = $livres
  tags = ["reservation-management"]
  guid = "reservation-availability-guid-001"
}