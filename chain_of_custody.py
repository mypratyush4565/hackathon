from db import get_connection

def log_action(evidence_id, action, user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_log (evidence_id, action, performed_by)
        VALUES (?, ?, ?)
    """, (evidence_id, action, user))

    conn.commit()
    conn.close()

def get_timeline(evidence_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT action, performed_by, timestamp
        FROM audit_log
        WHERE evidence_id = ?
        ORDER BY timestamp ASC
    """, (evidence_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

# Demo run
if __name__ == "__main__":
    evidence_id = 1

    log_action(evidence_id, "UPLOADED", "Police_Officer")
    log_action(evidence_id, "HASH_VERIFIED", "System")
    log_action(evidence_id, "ACCESSED", "Judge_1")
    log_action(evidence_id, "VERIFIED", "Judge_1")

    timeline = get_timeline(evidence_id)

    print("\nChain of Custody Timeline:")
    for action, user, time in timeline:
        print(f"{time} - {action} by {user}")


