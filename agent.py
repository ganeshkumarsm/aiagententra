import json
from openai import AzureOpenAI
import config

from tools.vm_tools import restart_vm, stop_vm
from tools.tool_registry import TOOLS
from permissions import is_vm_allowed
from audit import log_action

# Stores pending confirmations per user
pending_actions = {}

client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_KEY,
    azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-15-preview"
)


def run_agent(question, user, groups):

    session = user

    print(f"\n--- NEW REQUEST ---")
    print(f"User: {user}")
    print(f"Question: {question}")

    # ============================
    # 1️⃣ HANDLE CONFIRMATION FLOW
    # ============================

    if session in pending_actions:

        action = pending_actions[session]

        print("Pending action found:", action)
        print("User input:", question)

        if question.strip().lower() in ["yes", "y", "confirm", "ok"]:

            print("Executing action...")

            try:
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

                # remove only after success
                pending_actions.pop(session)

                log_action(user, action["type"], action["vm_name"])

                return result

            except Exception as e:
                print("ERROR executing action:", str(e))
                return f"Failed to execute action: {str(e)}"

        else:

            print("Action cancelled by user")
            pending_actions.pop(session)

            return "Action cancelled."

    # ============================
    # 2️⃣ LLM TOOL CALLING
    # ============================

    messages = [
        {
            "role": "system",
            "content": """
You are an Azure infrastructure assistant.

If the user asks to restart or stop a VM,
you MUST call the appropriate tool.

Always extract:
- vm_name
- resource_group
"""
        },
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    print("LLM response:", message)

    # ============================
    # 3️⃣ TOOL DETECTED
    # ============================

    if message.tool_calls:

        tool = message.tool_calls[0]

        print("Tool called:", tool.function.name)

        try:
            args = json.loads(tool.function.arguments)
        except Exception as e:
            print("JSON parse error:", str(e))
            return "Failed to parse tool arguments."

        vm_name = args.get("vm_name")
        resource_group = args.get("resource_group")

        print("Parsed args:", args)

        # ============================
        # 4️⃣ AUTHORIZATION CHECK
        # ============================

        if not is_vm_allowed(vm_name, groups):

            print("Authorization failed")
            return "You are not authorized to control this VM."

        # ============================
        # 5️⃣ STORE PENDING ACTION
        # ============================

        pending_actions[session] = {
            "type": "restart" if tool.function.name == "restart_vm" else "stop",
            "resource_group": resource_group,
            "vm_name": vm_name
        }

        print("Pending action stored:", pending_actions[session])

        return f"""
Planned action:

VM: {vm_name}
Resource Group: {resource_group}

⚠️ This will impact availability.

Confirm? (yes/no)
"""

    # ============================
    # 6️⃣ NORMAL RESPONSE
    # ============================

    return message.content