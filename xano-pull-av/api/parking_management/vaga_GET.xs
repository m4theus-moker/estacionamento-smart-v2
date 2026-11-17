query vaga verb=GET {
  api_group = "Parking Management"
  auth = "user"

  input {
    int? location_id
  }

  stack {
    db.query vaga {
      where = ($input.location_id == null || $db.vaga.location_id == $input.location_id)
      return = {type: "list"}
    } as $vagas
  }

  response = $vagas
  tags = ["parking-management"]
  guid = "vaga-get-guid-001"
}