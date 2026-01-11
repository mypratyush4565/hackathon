def check_parent_child(evidence, store):
    # If parent hash exists, verify parent is stored
    parent_hash = evidence.parent_hash
    if parent_hash and parent_hash not in [e['hash'] for e in store]:
        raise ValueError("Parent evidence not found in store")
    return True
