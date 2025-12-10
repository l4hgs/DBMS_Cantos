from db import get_connection

def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id, name FROM category ORDER BY category_id ASC")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def add_category(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO category (name) VALUES (%s)", (name,))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def get_category_by_id(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id, name FROM category WHERE category_id=%s", (category_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_category_id_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id FROM category WHERE name=%s", (name,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        cursor.close()
        conn.close()

def update_category(category_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE category SET name=%s WHERE category_id=%s", (new_name, category_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM category WHERE category_id=%s", (category_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
