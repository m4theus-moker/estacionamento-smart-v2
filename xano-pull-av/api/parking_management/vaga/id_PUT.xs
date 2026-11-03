query "vaga/{id}" verb=PUT {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
    int location_id
    text numero filters=trim
    enum tipo {
      values = ["carro", "moto", "pcd", "eletrico"]
    }
  
    enum status {
      values = ["livre", "ocupada", "reservada"]
    }
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record
  
    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem atualizar vagas."
    }
  
    db.get vaga {
      field_name = "id"
      field_value = $input.id
    } as $vaga
  
    precondition ($vaga != null) {
      error_type = "notfound"
      error = "Vaga não encontrada."
    }
  
    db.query vaga {
      where = $db.vaga.location_id == $input.location_id && $db.vaga.numero == $input.numero && $db.vaga.id != $input.id
      return = {type: "single"}
    } as $existing_vaga
  
    precondition ($existing_vaga == null) {
      error_type = "inputerror"
      error = "Já existe outra vaga cadastrada com este número neste local."
    }
  
    db.edit vaga {
      field_name = "id"
      field_value = $input.id
      data = {
        location_id: $input.location_id
        numero     : $input.numero
        tipo       : $input.tipo
        status     : $input.status
      }
    } as $updated_vaga
  }

  response = $updated_vaga
  tags = ["parking-management"]
  guid = "vaga-put-guid-001"
}