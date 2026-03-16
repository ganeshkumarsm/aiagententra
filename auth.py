import base64
import json
from flask import request


def get_user():

    return request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")


def get_user_groups():

    principal = request.headers.get("X-MS-CLIENT-PRINCIPAL")

    if not principal:
        return []

    decoded = base64.b64decode(principal)
    principal_data = json.loads(decoded)

    claims = principal_data["claims"]

    groups = []

    for claim in claims:
        if claim["typ"] == "groups":
            groups.append(claim["val"])

    return groups