query "location/{id}" verb=DELETE {
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
      error = "Acesso negado. Apenas administradores podem excluir locais."
    }
  
    db.get location {
      field_name = "id"
      field_value = $input.id
    } as $loc
  
    precondition ($loc != null) {
      error_type = "notfound"
      error = "Local não encontrado."
    }
  
    db.query vaga {
      where = $db.vaga.location_id == $input.id
      return = {type: "single"}
    } as $linked_vaga
  
    precondition ($linked_vaga == null) {
      error_type = "inputerror"
      error = "Não é possível excluir o local pois existem vagas vinculadas."
    }
  
    db.query tarifa {
      where = $db.tarifa.location_id == $input.id
      return = {type: "single"}
    } as $linked_tarifa
  
    precondition ($linked_tarifa == null) {
      error_type = "inputerror"
      error = "Não é possível excluir o local pois existem tarifas vinculadas."
    }
  
    db.del location {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    message: "Local excluído com sucesso."
  }

  tags = ["parking-management"]
  guid = "location-delete-guid-001"
}