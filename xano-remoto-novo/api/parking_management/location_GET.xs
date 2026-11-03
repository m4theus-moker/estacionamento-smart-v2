query location verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
  }

  stack {
    db.query location {
      return = {type: "list"}
    } as $locations
  }

  response = $locations
  tags = ["parking-management"]
  guid = "location-get-guid-001"
}