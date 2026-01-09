from db import get_connection, create_tables

# 🔹 Log any action
def log_action(evidence_id, action, user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO audit_log (evidence_id, action, performed_by) VALUES (?, ?, ?)",
        (evidence_id, action, user)
    )

    conn.commit()
    conn.close()

# 🔹 Get full chain-of-custody timeline
def get_timeline(evidence_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT action, performed_by, timestamp
        FROM audit_log
        WHERE evidence_id = ?
        ORDER BY timestamp
        """,
        (evidence_id,)
    )

    records = cursor.fetchall()
    conn.close()
    return records


# 🧪 DEMO (FOR JUDGES)
if __name__ == "__main__":
    create_tables()  # 🔥 MOST IMPORTANT LINE

    evidence_id = 1

    log_action(evidence_id, "UPLOAD", "Police_Officer_A")
    log_action(evidence_id, "HASH_VERIFIED", "System")
    log_action(evidence_id, "ACCESSED", "Judge_1")
    log_action(evidence_id, "VERIFIED", "Judge_1")

    print("\n📜 Chain of Custody Timeline:\n")

    timeline = get_timeline(evidence_id)

    for action, user, time in timeline:
        print(f"{time} → {action} by {user}")

