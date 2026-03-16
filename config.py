import os
from dotenv import load_dotenv

# Load .env file only for local development
load_dotenv()


# -----------------------------
# Azure OpenAI Configuration
# -----------------------------

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o")


# -----------------------------
# Azure AI Search Configuration
# -----------------------------

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")
SEARCH_INDEX = os.getenv("SEARCH_INDEX")


# -----------------------------
# Azure Infrastructure Access
# -----------------------------

AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")


# -----------------------------
# Security / Authorization
# -----------------------------

# optional: restrict allowed tenant
ALLOWED_TENANT_ID = os.getenv("ALLOWED_TENANT_ID")


# -----------------------------
# App Settings
# -----------------------------

APP_NAME = os.getenv("APP_NAME", "azure-ai-infra-agent")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# -----------------------------
# Safety Controls
# -----------------------------

# Require confirmation before executing actions
REQUIRE_CONFIRMATION = True

# Allowed operations
ALLOWED_ACTIONS = [
    "restart_vm",
    "stop_vm"
]