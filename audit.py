import datetime


def log_action(user, action, vm_name):

    timestamp = datetime.datetime.utcnow()

    print(f"{timestamp} | {user} | {action} | {vm_name}")