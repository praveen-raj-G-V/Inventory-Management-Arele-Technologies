from flask import Flask, render_template, request, redirect, url_for
from db_config import get_db_connection

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('view_products'))

@app.route('/products')
def view_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Product (name, description) VALUES (%s, %s)", (name, description))
        conn.commit()
        conn.close()
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        cursor.execute("UPDATE Product SET name=%s, description=%s WHERE product_id=%s", (name, description, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_products'))
    cursor.execute("SELECT * FROM Product WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product WHERE product_id=%s", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_products'))


@app.route('/locations')
def view_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Location")
    locations = cursor.fetchall()
    conn.close()
    return render_template('locations.html', locations=locations)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address', '')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Location (name, address) VALUES (%s, %s)", (name, address))
        conn.commit()
        conn.close()
        return redirect(url_for('view_locations'))
    return render_template('add_location.html')

@app.route('/edit_location/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address', '')
        cursor.execute("UPDATE Location SET name=%s, address=%s WHERE location_id=%s", (name, address, location_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_locations'))
    cursor.execute("SELECT * FROM Location WHERE location_id=%s", (location_id,))
    loc = cursor.fetchone()
    conn.close()
    return render_template('edit_location.html', location=loc)

@app.route('/delete_location/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Location WHERE location_id=%s", (location_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_locations'))


@app.route('/movements')
def view_movements():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.movement_id, p.name AS product_name,
               f.name AS from_loc, t.name AS to_loc, m.qty, m.timestamp
        FROM ProductMovement m
        LEFT JOIN Product p ON m.product_id = p.product_id
        LEFT JOIN Location f ON m.from_location = f.location_id
        LEFT JOIN Location t ON m.to_location = t.location_id
        ORDER BY m.timestamp DESC
    """)
    movements = cursor.fetchall()
    conn.close()
    return render_template('movements.html', movements=movements)

@app.route('/add_movement', methods=['GET', 'POST'])
def add_movement():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Location")
    locations = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form['qty'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ProductMovement (product_id, from_location, to_location, qty)
            VALUES (%s, %s, %s, %s)
        """, (product_id, from_location, to_location, qty))
        conn.commit()
        conn.close()
        return redirect(url_for('view_movements'))

    return render_template('add_movement.html', products=products, locations=locations)


@app.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.product_id,
            p.name AS Product,
            l.location_id,
            l.name AS Warehouse,
            COALESCE(SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0) AS Qty
        FROM Product p
        CROSS JOIN Location l
        LEFT JOIN ProductMovement pm ON pm.product_id = p.product_id
        GROUP BY p.product_id, p.name, l.location_id, l.name
        HAVING Qty <> 0
        ORDER BY p.name, l.name
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template('report.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)