query tarifa verb=POST {
  api_group = "Parking Management"
  auth = "user"

  input {
    int location_id
    enum tipo_vaga {
      values = ["carro", "moto", "pcd", "eletrico"]
    }
  
    decimal valor_hora
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["role"]
    } as $user_record
  
    precondition ($user_record != null && $user_record.role == "admin") {
      error_type = "accessdenied"
      error = "Acesso negado. Apenas administradores podem gerenciar tarifas."
    }
  
    precondition ($input.valor_hora > 0) {
      error_type = "inputerror"
      error = "O valor da hora deve ser maior que zero."
    }
  
    db.query tarifa {
      where = $db.tarifa.location_id == $input.location_id && $db.tarifa.tipo_vaga == $input.tipo_vaga
      return = {type: "single"}
    } as $existing
  
    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Já existe uma tarifa cadastrada para este tipo de vaga neste local."
    }
  
    db.add tarifa {
      data = {
        created_at : "now"
        location_id: $input.location_id
        tipo_vaga  : $input.tipo_vaga
        valor_hora : $input.valor_hora
      }
    } as $tarifa
  }

  response = $tarifa
  tags = ["parking-management"]
  guid = "tarifa-post-guid-001"
}