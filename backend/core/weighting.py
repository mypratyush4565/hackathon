from backend.config.rules import SOURCE_WEIGHTS

def calculate_weight(source_type):
    return SOURCE_WEIGHTS.get(source_type, 1)  # default weight 1
