query "admin/reservation" verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int? location_id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record
  
    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem listar todas as reservas."
    }
  
    db.query reservation {
      where = ($input.location_id == null || $db.reservation.location_id == $input.location_id)
      return = {type: "list"}
    } as $reservations
  }

  response = $reservations
  tags = ["reservation-management"]
  guid = "admin-reservation-get-guid-001"
}