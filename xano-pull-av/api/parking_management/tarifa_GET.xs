query tarifa verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int? location_id
  }

  stack {
    db.query tarifa {
      where = ($input.location_id == null || $db.tarifa.location_id == $input.location_id)
      return = {type: "list"}
    } as $tarifas
  }

  response = $tarifas
  tags = ["parking-management"]
  guid = "tarifa-get-guid-001"
}