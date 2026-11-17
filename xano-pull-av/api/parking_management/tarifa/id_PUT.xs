query "tarifa/{id}" verb=PUT {
  api_group = "Parking Management"
  auth = "user"

  input {
    int id
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
      error = "Acesso negado. Apenas administradores podem atualizar tarifas."
    }
  
    precondition ($input.valor_hora > 0) {
      error_type = "inputerror"
      error = "O valor da hora deve ser maior que zero."
    }
  
    db.get tarifa {
      field_name = "id"
      field_value = $input.id
    } as $tarifa
  
    precondition ($tarifa != null) {
      error_type = "notfound"
      error = "Tarifa não encontrada."
    }
  
    db.query tarifa {
      where = $db.tarifa.location_id == $input.location_id && $db.tarifa.tipo_vaga == $input.tipo_vaga && $db.tarifa.id != $input.id
      return = {type: "single"}
    } as $existing_tarifa
  
    precondition ($existing_tarifa == null) {
      error_type = "inputerror"
      error = "Já existe outra tarifa cadastrada para este tipo de vaga neste local."
    }
  
    db.edit tarifa {
      field_name = "id"
      field_value = $input.id
      data = {
        location_id: $input.location_id
        tipo_vaga  : $input.tipo_vaga
        valor_hora : $input.valor_hora
      }
    } as $updated_tarifa
  }

  response = $updated_tarifa
  tags = ["parking-management"]
  guid = "tarifa-put-guid-001"
}