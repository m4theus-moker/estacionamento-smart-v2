query reservation verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
  }

  stack {
    db.query reservation {
      where = $db.reservation.user_id == $auth.id
      return = {type: "list"}
    } as $reservations
  }

  response = $reservations
  tags = ["reservation-management"]
  guid = "reservation-get-guid-001"
}