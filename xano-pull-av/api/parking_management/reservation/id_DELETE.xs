query "reservation/{id}" verb=DELETE {
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
      error = "Reserva não encontrada ou sem permissão."
    }
  
    // Update reservation status to cancelada
    db.edit reservation {
      field_name = "id"
      field_value = $input.id
      data = {status: "cancelada"}
    } as $updated
  
    // Release vaga status if it was reservada
    db.get vaga {
      field_name = "id"
      field_value = $reservation.vaga_id
    } as $vaga
  
    conditional {
      if ($vaga != null && $vaga.status == "reservada") {
        db.edit vaga {
          field_name = "id"
          field_value = $reservation.vaga_id
          data = {status: "livre"}
        } as $released_vaga
      }
    }
  }

  response = {
    success: true
    message: "Reserva cancelada com sucesso."
  }

  tags = ["reservation-management"]
  guid = "reservation-delete-guid-001"
}