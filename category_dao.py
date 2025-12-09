"""
category_dao.py
Data Access Object (DAO) for the `categories` table.
Provides simple functions to list/add/update/delete categories.
"""

from db import get_connection

def get_all_categories():
    """
    Return a list of categories as tuples: (category_id, name).
    Suitable for populating comboboxes and lookups.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id, name FROM categories ORDER BY name")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def add_category(name):
    """
    Add a new category.
    Returns the inserted category_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def get_category_by_id(category_id):
    """
    Return a single category tuple (category_id, name) or None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id, name FROM categories WHERE category_id=%s", (category_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_category_id_by_name(name):
    """
    Return category_id for a given category name, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id FROM categories WHERE name=%s", (name,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        cursor.close()
        conn.close()

def update_category(category_id, new_name):
    """
    Update a category's name.
    Returns True if a row was updated, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categories SET name=%s WHERE category_id=%s", (new_name, category_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()

def delete_category(category_id):
    """
    Delete a category. Note: transactions referencing this category will be cascade-deleted
    only if the foreign key ON DELETE CASCADE is set (our SQL uses CASCADE).
    Returns True if a row was deleted.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM categories WHERE category_id=%s", (category_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
