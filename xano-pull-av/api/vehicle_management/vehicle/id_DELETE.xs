query "vehicle/{id}" verb=DELETE {
  api_group = "Vehicle Management"
  auth = "user"

  input {
    int id
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
  
    // Delete vehicle record
    db.del vehicle {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    message: "Veículo excluído com sucesso."
  }

  tags = ["vehicle-management"]
  guid = "vehicle-delete-guid-001"
}