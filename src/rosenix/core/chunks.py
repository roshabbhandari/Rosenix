def chunks(items, size):
    if size < 1:
        raise ValueError("size must be positive")
    batch=[]
    for item in items:
        batch.append(item)
        if len(batch)==size:
            yield batch
            batch=[]
    if batch:
        yield batch
