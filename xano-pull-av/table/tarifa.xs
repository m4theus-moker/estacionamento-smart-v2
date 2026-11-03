table tarifa {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int location_id
    enum tipo_vaga {
      values = ["carro", "moto", "pcd", "eletrico"]
    }
  
    decimal valor_hora
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "location_id", op: "asc"}]}
    {
      type : "btree|unique"
      field: [
        {name: "location_id", op: "asc"}
        {name: "tipo_vaga", op: "asc"}
      ]
    }
  ]

  tags = ["parking-management"]
  guid = "tarifa-table-guid-001"
}