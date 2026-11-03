query "admin/reservation/{id}" verb=DELETE {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record

    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem cancelar qualquer reserva."
    }

    db.get reservation {
      field_name = "id"
      field_value = $input.id
    } as $reservation

    precondition ($reservation != null) {
      error_type = "notfound"
      error = "Reserva não encontrada."
    }

    precondition ($reservation.status != "cancelada") {
      error_type = "inputerror"
      error = "Esta reserva já está cancelada."
    }

    precondition ($reservation.end_time > now()) {
      error_type = "inputerror"
      error = "Não é possível cancelar uma reserva cujo horário de término já passou."
    }

    db.edit reservation {
      field_name = "id"
      field_value = $input.id
      data = {status: "cancelada"}
    } as $updated
  }

  response = {
    success: true
    message: "Reserva cancelada pelo administrador com sucesso."
  }

  tags = ["reservation-management"]
  guid = "admin-reservation-delete-guid-001"
}
