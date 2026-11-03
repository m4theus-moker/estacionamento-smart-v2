query "vehicle/{id}" verb=PUT {
  api_group = "Vehicle Management"
  auth = "user"

  input {
    int id
    text plate filters=trim|upper
    text brand filters=trim
    text model filters=trim
    text color filters=trim
    int year
  }

  stack {
    // Get vehicle by id and ensure strict user ownership validation
    db.get vehicle {
      field_name = "id"
      field_value = $input.id
    } as $vehicle
  
    precondition ($vehicle != null && $vehicle.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Veículo não encontrado ou acesso negado."
    }
  
    // Update vehicle data
    db.edit vehicle {
      field_name = "id"
      field_value = $input.id
      data = {
        plate: $input.plate
        brand: $input.brand
        model: $input.model
        color: $input.color
        year : $input.year
      }
    } as $updated_vehicle
  }

  response = $updated_vehicle
  tags = ["vehicle-management"]
  guid = "vehicle-put-guid-001"
}