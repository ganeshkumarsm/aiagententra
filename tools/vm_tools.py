from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import config

credential = DefaultAzureCredential()

compute_client = ComputeManagementClient(
    credential,
    config.AZURE_SUBSCRIPTION_ID
)


def restart_vm(resource_group, vm_name):

    compute_client.virtual_machines.begin_restart(
        resource_group,
        vm_name
    )

    return f"Restart initiated for {vm_name}"


def stop_vm(resource_group, vm_name):

    compute_client.virtual_machines.begin_deallocate(
        resource_group,
        vm_name
    )

    return f"Shutdown initiated for {vm_name}"