query "tarifa/{id}" verb=DELETE {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record
  
    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem excluir tarifas."
    }
  
    db.get tarifa {
      field_name = "id"
      field_value = $input.id
    } as $tarifa
  
    precondition ($tarifa != null) {
      error_type = "notfound"
      error = "Tarifa não encontrada."
    }
  
    db.del tarifa {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    message: "Tarifa excluída com sucesso."
  }

  tags = ["parking-management"]
  guid = "tarifa-delete-guid-001"
}