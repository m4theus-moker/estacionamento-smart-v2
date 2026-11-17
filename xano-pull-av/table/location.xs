table location {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    text address filters=trim
    text description filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "name", op: "asc"}]}
  ]

  tags = ["parking-management"]
  guid = "location-table-guid-001"
}