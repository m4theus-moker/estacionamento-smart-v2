table reservation {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int user_id
    int location_id
    int vaga_id
    int vehicle_id
    timestamp start_time
    timestamp end_time
    enum status {
      values = ["ativa", "cancelada", "concluida"]
    }
  
    decimal price
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "location_id", op: "asc"}]}
    {type: "btree", field: [{name: "vaga_id", op: "asc"}]}
  ]

  tags = ["reservation-management"]
  guid = "reservation-table-guid-001"
}