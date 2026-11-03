query vehicle verb=POST {
  api_group = "Vehicle Management"
  auth = "user"

  input {
    text plate filters=trim|upper
    text brand filters=trim
    text model filters=trim
    text color filters=trim
    int year
  }

  stack {
    // Check if vehicle with plate already exists
    db.get vehicle {
      field_name = "plate"
      field_value = $input.plate
    } as $existing
  
    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Já existe um veículo cadastrado com esta placa."
    }
  
    // Create vehicle associated with authenticated user
    db.add vehicle {
      data = {
        created_at: "now"
        user_id   : $auth.id
        plate     : $input.plate
        brand     : $input.brand
        model     : $input.model
        color     : $input.color
        year      : $input.year
      }
    } as $vehicle
  }

  response = $vehicle
  tags = ["vehicle-management"]
  guid = "vehicle-post-guid-001"
}