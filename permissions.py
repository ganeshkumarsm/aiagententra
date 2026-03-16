GROUP_VM_PERMISSIONS = {

    "AI-Infra-Operators": [
        "teams",
        "vm-test-01"
    ],

    "AI-Infra-Admins": [
        "teams",
        "vm-prod-02"
    ]
}


def is_vm_allowed(vm_name, groups):

    for g in groups:

        if g in GROUP_VM_PERMISSIONS:

            if vm_name in GROUP_VM_PERMISSIONS[g]:
                return True

    return False