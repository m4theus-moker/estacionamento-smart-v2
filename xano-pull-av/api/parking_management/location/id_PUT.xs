query "location/{id}" verb=PUT {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
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
      error = "Acesso negado. Apenas administradores podem atualizar locais."
    }
  
    db.get location {
      field_name = "id"
      field_value = $input.id
    } as $loc
  
    precondition ($loc != null) {
      error_type = "notfound"
      error = "Local não encontrado."
    }
  
    db.query location {
      where = $db.location.name == $input.name && $db.location.id != $input.id
      return = {type: "single"}
    } as $existing_name
  
    precondition ($existing_name == null) {
      error_type = "inputerror"
      error = "Já existe outro local cadastrado com este nome."
    }
  
    db.edit location {
      field_name = "id"
      field_value = $input.id
      data = {
        name       : $input.name
        address    : $input.address
        description: $input.description
      }
    } as $updated
  }

  response = $updated
  tags = ["parking-management"]
  guid = "location-put-guid-001"
}