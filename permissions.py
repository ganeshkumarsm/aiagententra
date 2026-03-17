GROUP_VM_PERMISSIONS = {

    "b7dcea9c-bdab-4352-84f3-cb5a7f8aa456": [
        "teams",
        "vm-test-01"
    ],

    "AI-Infra-Admins": [
        "teams",
        "vm-prod-02"
    ]
}


def is_vm_allowed(vm_name, groups):

    for group_id in groups:

        if group_id in GROUP_VM_PERMISSIONS:

            if vm_name in GROUP_VM_PERMISSIONS[group_id]:
                return True

    return False