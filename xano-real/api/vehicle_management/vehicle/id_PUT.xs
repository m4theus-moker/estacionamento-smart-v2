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
    text type? filters=trim|lower
  }

  stack {
    precondition ($input.type == null || $input.type == "" || $input.type == "carro" || $input.type == "moto" || $input.type == "pcd") {
      error_type = "inputerror"
      error = "Tipo de veículo inválido. Valores aceitos: carro, moto, pcd."
    }

    // Get vehicle by id and ensure strict user ownership validation
    db.get vehicle {
      field_name = "id"
      field_value = $input.id
    } as $vehicle
  
    precondition ($vehicle != null && $vehicle.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Veículo não encontrado ou acesso negado."
    }
  
    // Update vehicle data, preserving type if omitted
    db.edit vehicle {
      field_name = "id"
      field_value = $input.id
      data = {
        plate: $input.plate
        brand: $input.brand
        model: $input.model
        color: $input.color
        year : $input.year
        type : ($input.type != null && $input.type != "") ? $input.type : $vehicle.type
      }
    } as $updated_vehicle
  }

  response = $updated_vehicle
  tags = ["vehicle-management"]
  guid = "vehicle-put-guid-001"
}
