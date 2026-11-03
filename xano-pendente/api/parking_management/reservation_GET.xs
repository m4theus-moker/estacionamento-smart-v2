query reservation verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int? location_id
  }

  stack {
    db.query reservation {
      where = ($input.location_id == null || $db.reservation.location_id == $input.location_id) && ($db.reservation.user_id == $auth.id)
      return = {type: "list"}
    } as $reservations
  }

  response = $reservations
  tags = ["reservation-management"]
  guid = "reservation-get-guid-001"
}