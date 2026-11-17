query "vaga/{id}" verb=DELETE {
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
      error = "Acesso negado. Apenas administradores podem excluir vagas."
    }
  
    db.get vaga {
      field_name = "id"
      field_value = $input.id
    } as $vaga
  
    precondition ($vaga != null) {
      error_type = "notfound"
      error = "Vaga não encontrada."
    }
  
    db.del vaga {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    message: "Vaga excluída com sucesso."
  }

  tags = ["parking-management"]
  guid = "vaga-delete-guid-001"
}