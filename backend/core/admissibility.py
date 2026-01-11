def compute_admissibility_score(evidence_weight, custody_completeness):
    # Score 0-100 based on weight and custody
    score = min(100, int(evidence_weight * 50 + custody_completeness * 50))
    return score
