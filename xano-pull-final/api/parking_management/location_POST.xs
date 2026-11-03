query location verb=POST {
  api_group = "Parking Management"
  auth = "user"

  input {
    text name filters=trim
    text address filters=trim
    text description filters=trim
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record
  
    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem gerenciar locais."
    }
  
    db.get location {
      field_name = "name"
      field_value = $input.name
    } as $existing
  
    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Já existe um local cadastrado com este nome."
    }
  
    db.add location {
      data = {
        created_at : "now"
        name       : $input.name
        address    : $input.address
        description: $input.description
      }
    } as $location
  }

  response = $location
  tags = ["parking-management"]
  guid = "location-post-guid-001"
}