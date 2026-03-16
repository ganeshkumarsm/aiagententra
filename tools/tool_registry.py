TOOLS = [

{
"type": "function",
"function": {
"name": "restart_vm",
"description": "Restart an Azure virtual machine",
"parameters": {
"type": "object",
"properties": {
"resource_group": {"type": "string"},
"vm_name": {"type": "string"}
},
"required": ["resource_group", "vm_name"]
}
}
},

{
"type": "function",
"function": {
"name": "stop_vm",
"description": "Stop an Azure virtual machine",
"parameters": {
"type": "object",
"properties": {
"resource_group": {"type": "string"},
"vm_name": {"type": "string"}
},
"required": ["resource_group", "vm_name"]
}
}
}

]