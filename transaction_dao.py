from db import get_connection

def add_transaction(type, category_id, amount, date, note):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO transactions (type, category_id, amount, trans_date, note) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (type, category_id, amount, date, note))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.trans_id, t.type, c.name, t.amount, t.trans_date, t.note
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        ORDER BY t.trans_id ASC
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def update_transaction(trans_id, type, category_id, amount, date, note):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE transactions 
             SET type=%s, category_id=%s, amount=%s, trans_date=%s, note=%s
             WHERE trans_id=%s"""
    cursor.execute(sql, (type, category_id, amount, date, note, trans_id))
    conn.commit()
    conn.close()

def delete_transaction(trans_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE trans_id=%s", (trans_id,))
    conn.commit()
    conn.close()
