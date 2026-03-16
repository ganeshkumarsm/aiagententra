import json
from openai import AzureOpenAI
import config

from tools.vm_tools import restart_vm, stop_vm
from tools.tool_registry import TOOLS
from permissions import is_vm_allowed
from audit import log_action

pending_actions = {}

client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)


def run_agent(question, user, groups):

    session = user

    if session in pending_actions:

        action = pending_actions.pop(session)

        if question.lower() == "yes":

            if action["type"] == "restart":

                result = restart_vm(
                    action["resource_group"],
                    action["vm_name"]
                )

            else:

                result = stop_vm(
                    action["resource_group"],
                    action["vm_name"]
                )

            log_action(user, action["type"], action["vm_name"])

            return result

        return "Action cancelled."


    messages = [
        {
            "role": "system",
            "content": """
You are an Azure infrastructure assistant.

If the user asks to restart or stop a VM,
use the appropriate tool.
"""
        },
        {"role": "user", "content": question}
    ]


    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=messages,
        tools=TOOLS
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool = message.tool_calls[0]

        args = json.loads(tool.function.arguments)

        vm_name = args["vm_name"]

        if not is_vm_allowed(vm_name, groups):

            return "You are not authorized to control this VM."

        pending_actions[session] = {

            "type": "restart" if tool.function.name == "restart_vm" else "stop",
            "resource_group": args["resource_group"],
            "vm_name": vm_name
        }

        return f"""
Planned action:

VM: {vm_name}
Resource Group: {args['resource_group']}

Confirm? (yes/no)
"""

    return message.content