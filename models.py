from database import fetch_all, execute

### CATEGORY FUNCTIONS ###

def get_categories():
    return fetch_all("SELECT category_name FROM category")

### TRANSACTION FUNCTIONS ###

def add_transaction(category, amount, ttype, date, notes):
    cat_id = fetch_all("SELECT category_id FROM category WHERE category_name=%s", (category,))
    
    if not cat_id:
        return
        
    sql = """
        INSERT INTO transaction_tbl (category_id, amount, type, date, notes)
        VALUES (%s,%s,%s,%s,%s)
    """
    params = (cat_id[0][0], amount, ttype, date, notes)
    execute(sql, params)

def update_transaction(tid, amount, notes):
    sql = "UPDATE transaction_tbl SET amount=%s, notes=%s WHERE transaction_id=%s"
    execute(sql, (amount, notes, tid))

def delete_transaction(tid):
    sql = "DELETE FROM transaction_tbl WHERE transaction_id=%s"
    execute(sql, (tid,))

def get_all_transactions():
    query = """
        SELECT t.transaction_id, c.category_name, t.type, t.amount, t.date, t.notes
        FROM transaction_tbl t
        JOIN category c ON t.category_id = c.category_id
        ORDER BY t.date DESC
    """
    return fetch_all(query)

def get_filtered_transactions(start_date, end_date):
    query = """
        SELECT t.transaction_id, c.category_name, t.type, t.amount, t.date, t.notes
        FROM transaction_tbl t
        JOIN category c ON t.category_id = c.category_id
        WHERE t.date BETWEEN %s AND %s
        ORDER BY t.date DESC
    """
    return fetch_all(query, (start_date, end_date))

def get_total_balance(start_date=None, end_date=None):
    if start_date and end_date:
        query = """
            SELECT 
            SUM(CASE WHEN type='Income' THEN amount ELSE -amount END) AS balance
            FROM transaction_tbl
            WHERE date BETWEEN %s AND %s
        """
        result = fetch_all(query, (start_date, end_date))
    else:
        query = """
            SELECT 
            SUM(CASE WHEN type='Income' THEN amount ELSE -amount END) AS balance
            FROM transaction_tbl
        """
        result = fetch_all(query)

    return result[0][0] if result[0][0] else 0
