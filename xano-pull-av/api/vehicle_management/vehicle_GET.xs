query vehicle verb=GET {
  api_group = "Vehicle Management"
  auth = "user"

  input {
  }

  stack {
    // Retrieve vehicles strictly filtered by authenticated user id
    db.query vehicle {
      where = $db.vehicle.user_id == $auth.id
      return = {type: "list"}
    } as $vehicles
  }

  response = $vehicles
  tags = ["vehicle-management"]
  guid = "vehicle-get-guid-001"
}