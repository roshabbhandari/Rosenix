def copy_record(record):
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")
    return dict(record)


def project(record, fields):
    return {field: record[field] for field in fields if field in record}
