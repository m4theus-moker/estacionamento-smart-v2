query vaga verb=POST {
  api_group = "Parking Management"
  auth = "user"

  input {
    int location_id
    text numero filters=trim
    enum tipo {
      values = ["carro", "moto", "pcd", "eletrico"]
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
      error = "Acesso negado. Apenas administradores podem gerenciar vagas."
    }
  
    db.query vaga {
      where = $db.vaga.location_id == $input.location_id && $db.vaga.numero == $input.numero
      return = {type: "single"}
    } as $existing
  
    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Já existe uma vaga cadastrada com este número neste local."
    }
  
    db.add vaga {
      data = {
        created_at : "now"
        location_id: $input.location_id
        numero     : $input.numero
        tipo       : $input.tipo
        status     : "livre"
      }
    } as $vaga
  }

  response = $vaga
  tags = ["parking-management"]
  guid = "vaga-post-guid-001"
}