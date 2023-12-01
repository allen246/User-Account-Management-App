import uuid


def generate_uuid_with_prefix(prefix):
    _id = str(uuid.uuid4()).replace("-", "")
    return f"{prefix}{_id[len(prefix):]}"
