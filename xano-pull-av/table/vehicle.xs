table vehicle {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int user_id
    text plate filters=trim|upper
    text brand filters=trim
    text model filters=trim
    text color filters=trim
    int year
    enum type? {
      values = ["carro", "moto", "pcd"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree|unique", field: [{name: "plate", op: "asc"}]}
  ]

  tags = ["vehicle-management"]
  guid = "vehicle-table-guid-001"
}