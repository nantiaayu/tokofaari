from flask import Flask, Response, render_template, redirect, url_for, request, flash,  abort, send_file
from flask_mysqldb import MySQL
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import seaborn as sns
from sklearn.metrics import mean_absolute_error
from datetime import datetime
import pdfkit
from functools import wraps
from flask import abort
from werkzeug.utils import secure_filename
from functools import wraps
from flask import session
from math import ceil
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import pickle
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from io import BytesIO
import mysql.connector.errors
from mysql.connector import Error

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.urandom(24)  # Atur secret key untuk keamanan sesi
# folder untuk gambar admin
app.config['UPLOAD_FOLDER'] = 'static/admin/gambar_product/'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maksimal 16MB

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    if user:
        print(f"Loading user: {user}")  # Debugging statement
        return User(user[0], user[1], user[5])  # Pastikan user[5] adalah kolom yang valid untuk level_akses
    print("User not found in load_user")  # Debugging statement
    return None

# Ensure the upload folder exists
if not os.path.exists('static/admin/gambarpackages'):
    os.makedirs('static/admin/gambarpackages')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def home():
    return render_template('home.php')

@app.route('/tentang')
def tentang():
    return render_template('about.php')


@app.route('/produk')
@login_required
def produk():
    if current_user.role not in ['admin', 'customer']:
        abort(403)
    
    cur = mysql.connection.cursor()

    # Pagination for packages
    page_packages = request.args.get('page_packages', 1, type=int)
    per_page = 9
    offset_packages = (page_packages - 1) * per_page

    cur.execute("SELECT COUNT(*) FROM package")
    total_packages = cur.fetchone()[0]
    cur.execute("SELECT * FROM package LIMIT %s OFFSET %s", (per_page, offset_packages))
    packages = cur.fetchall()
    
    pagination_packages = {
        'total_pages': ceil(total_packages / per_page),
        'current_page': page_packages,
        'has_prev': page_packages > 1,
        'has_next': page_packages < ceil(total_packages / per_page)
    }

    # Pagination for products
    page_products = request.args.get('page_products', 1, type=int)
    offset_products = (page_products - 1) * per_page

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]
    cur.execute("SELECT * FROM products LIMIT %s OFFSET %s", (per_page, offset_products))
    products = cur.fetchall()
    
    pagination_products = {
        'total_pages': ceil(total_products / per_page),
        'current_page': page_products,
        'has_prev': page_products > 1,
        'has_next': page_products < ceil(total_products / per_page)
    }

    return render_template(
        'products.php', 
        packages=packages, 
        products=products, 
        pagination_packages=pagination_packages, 
        pagination_products=pagination_products
    )
    
@app.route('/manager')
@login_required
@role_required('manager')
def manager():
    
    cur = mysql.connection.cursor()

    # Get total number of products
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # Get total number of transactions
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cur.fetchone()[0]

    # Get total sales amount
    cur.execute("SELECT SUM(total_price) FROM transactions")
    total_sales = cur.fetchone()[0] or 0

    # Get total quantity sold
    cur.execute("SELECT SUM(quantity) FROM transactions")
    total_quantity_sold = cur.fetchone()[0] or 0

    cur.close()

    # Pass the user's name and statistics to the template
    return render_template(
        'manager/index.php', 
        username=current_user.username, 
        total_products=total_products, 
        total_transactions=total_transactions, 
        total_sales=total_sales, 
        total_quantity_sold=total_quantity_sold
    )
@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    
    cur = mysql.connection.cursor()

    # Get total number of products
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # Get total number of transactions
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cur.fetchone()[0]

    # Get total sales amount
    cur.execute("SELECT SUM(total_price) FROM transactions")
    total_sales = cur.fetchone()[0] or 0

    # Get total quantity sold
    cur.execute("SELECT SUM(quantity) FROM transactions")
    total_quantity_sold = cur.fetchone()[0] or 0

    cur.close()

    # Pass the user's name and statistics to the template
    return render_template(
        'admin/index.php', 
        username=current_user.username, 
        total_products=total_products, 
        total_transactions=total_transactions, 
        total_sales=total_sales, 
        total_quantity_sold=total_quantity_sold
    )

# CRUD routes for Transaksi
@app.route('/transaksi/<string:type>/<int:id>', methods=['GET', 'POST'])
@login_required
def transaksi(type, id):
    cur = mysql.connection.cursor()
    
    if type == 'product':
        cur.execute("SELECT * FROM products WHERE id_products = %s", (id,))
        item = cur.fetchone()
        if not item:
            abort(404)
        item_type = 'product'
        item_price = float(item[2])  # Make sure to convert to float
        item_image = item[3]
        item_description = item[4]
        item_discount = 0
    elif type == 'package':
        cur.execute("SELECT * FROM package WHERE id_package = %s", (id,))
        item = cur.fetchone()
        if not item:
            abort(404)
        item_type = 'package'
        item_price = float(item[2])  # Make sure to convert to float
        item_image = item[3]  # Assuming image is the fifth column
        item_discount = float(item[4])  # Make sure to convert to float
        item_description = None  # Assuming package does not have a description
    else:
        abort(404)
    
    if request.method == 'POST':
        # Get quantity from form
        quantity = int(request.form['quantity'])
        
        if item_type == 'package' and item_discount:
            total_price = quantity * item_price * (1 - item_discount / 100)
        else:
            total_price = quantity * item_price
        
        # Insert transaction into database
        try:
            cur.execute("""
                INSERT INTO transactions (id, item_type, item_id, quantity, total_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (current_user.id, item_type, id, quantity, total_price))
            mysql.connection.commit()
            
            # Store transaction details in session
            session['transaction_success'] = {
                'name': item[1],
                'quantity': quantity,
                'total_price': total_price
            }
            
            return redirect(url_for('transaksi_success'))
        except Exception as e:
            mysql.connection.rollback()
            flash('Error processing transaction: ' + str(e))
            return redirect(url_for('transaksi', type=type, id=id))
    
    item_data = {
        'id': id,
        'name': item[1],
        'price': item_price,
        'discount': item_discount,
        'gambar': item_image,
        'description': item_description if item_description else ''
    }
    
    return render_template('transaksi.php', item=item_data, type=type)


@app.route('/transaksi_success')
@login_required
def transaksi_success():
    if 'transaction_success' not in session:
        return redirect(url_for('produk'))
    
    transaction_success = session.pop('transaction_success')  # Remove from session after retrieving
    
    return render_template('transaksi_success.php', transaction=transaction_success)

# CRUD routes for Customer Admin
@app.route('/produk/<int:id>', methods=['GET'])
@login_required
def produk_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id_products = %s", (id,))
    product = cur.fetchone()
    
    if not product:
        abort(404)
    
    product_data = {
        'id_products': product[0],
        'nama_products': product[1],
        'price': product[2],
        'gambar_products': product[3],
        'description': product[4]
    }
    
    return render_template('product_detail.php', product=product_data)

# CRUD routes for history Pembelian
@app.route('/purchase_history')
@login_required
def purchase_history():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.id_transactions, 
               COALESCE(p.nama_products, pk.name_package) AS item_name, 
               t.quantity, 
               t.total_price, 
               t.transaction_date
        FROM transactions t
        LEFT JOIN products p ON t.item_type = 'product' AND t.item_id = p.id_products
        LEFT JOIN package pk ON t.item_type = 'package' AND t.item_id = pk.id_package
        WHERE t.id = %s  -- assuming t.id is the column for user ID
        ORDER BY t.transaction_date DESC
    """, (current_user.id,))
    transactions = cur.fetchall()
    
    return render_template('purchase_history.php', transactions=transactions)




# CRUD routes for Package
@app.route('/admin/packages')
@login_required
@role_required('admin')
def admin_packages():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM package")
    packages = cur.fetchall()
    return render_template('admin/packages.php', packages=packages)

@app.route('/admin/add_package', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_package():
    if request.method == 'POST':
        name_package = request.form['name_package']
        total_price = request.form['total_price']
        discount = request.form['discount']

        if 'gambar_packages' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)

        file = request.files['gambar_packages']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/admin/gambarpackages', filename)
            file.save(file_path)

            cur = mysql.connection.cursor()
            try:
                cur.execute("""
                    INSERT INTO package (name_package, total_price, discount, gambar_packages)
                    VALUES (%s, %s, %s, %s)
                """, (name_package, total_price, discount, filename))
                mysql.connection.commit()
                
                flash('Package added successfully')
                return redirect(url_for('admin_packages'))
            except Exception as e:
                flash('Error adding package: ' + str(e))
                mysql.connection.rollback()
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)
    
    return render_template('admin/add_package.php')

@app.route('/admin/packages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_package(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM package WHERE id_package = %s", (id,))
    package = cur.fetchone()
    
    if request.method == 'POST':
        name_package = request.form['name_package']
        total_price = request.form['total_price']
        discount = request.form['discount']
        gambar_packages = package[4]  # Keep the old image by default

        if 'gambar_packages' in request.files:
            file = request.files['gambar_packages']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/admin/gambarpackages', filename))
                gambar_packages = filename

        cur.execute("""
            UPDATE package
            SET name_package = %s, total_price = %s, discount = %s, gambar_packages = %s
            WHERE id_package = %s
        """, (name_package, total_price, discount, gambar_packages, id))
        mysql.connection.commit()
        
        flash('Package updated successfully')
        return redirect(url_for('admin_packages'))
    
    package_data = {
        'id_package': package[0],
        'name_package': package[1],
        'total_price': package[2],
        'discount': package[4],
        'gambar_packages': package[3]
    }
    
    return render_template('admin/edit_package.php', package=package_data)

@app.route('/admin/packages/delete/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_package(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM package WHERE id_package = %s", (id,))
    mysql.connection.commit()
    flash('Package deleted successfully')
    return redirect(url_for('admin_packages'))

@app.route('/package_detail/<int:id>', methods=['GET'])
@login_required
def package_detail(id):
    cur = mysql.connection.cursor()
    
    # Get package details
    cur.execute("SELECT * FROM package WHERE id_package = %s", (id,))
    package = cur.fetchone()
    
    if not package:
        abort(404)
    
    # Get products associated with the package
    cur.execute("""
        SELECT p.id_products, p.nama_products, p.price, p.gambar_products, pp.quantity
        FROM package_products pp
        JOIN products p ON pp.id_products = p.id_products
        WHERE pp.id_package = %s
    """, (id,))
    products = cur.fetchall()
    
    package_data = {
        'id_package': package[0],
        'name_package': package[1],
        'total_price': package[2],
        'discount': package[4],
        'gambar_package': package[3],
        'products': products
    }
    
    return render_template('package_detail.php', package=package_data)



# CRUD routes for PackageProduct
@app.route('/admin/packages/<int:id>/products')
@login_required
@role_required('admin')
def package_products(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT pp.id, p.nama_products, pp.quantity FROM package_products pp JOIN products p ON pp.id_products = p.id_products WHERE pp.id_package = %s", (id,))
    package_products = cur.fetchall()
    return render_template('admin/package_products.php', package_id=id, package_products=package_products)

@app.route('/admin/packages/<int:id>/add_product', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_product_to_package(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    
    if request.method == 'POST':
        id_products = request.form['id_products']
        quantity = request.form['quantity']
        
        cur.execute("""
            INSERT INTO package_products (id_package, id_products, quantity)
            VALUES (%s, %s, %s)
        """, (id, id_products, quantity))
        mysql.connection.commit()
        
        flash('Product added to package successfully')
        return redirect(url_for('package_products', id=id))
    
    return render_template('admin/add_product_to_package.php', package_id=id, products=products)

@app.route('/admin/packages/<int:id>/products/delete/<int:id_products>', methods=['POST'])
@login_required
@role_required('admin')
def delete_product_from_package(id, id_products):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM package_products WHERE id = %s", (id_products,))
    mysql.connection.commit()
    flash('Product removed from package successfully')
    return redirect(url_for('package_products', id=id))


# CRUD routes for Users_admin
@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, nama, no_telp, level_akses FROM users")
    users = cur.fetchall()
    return render_template('admin/admin_users.php', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        no_telp = request.form['no_telp']
        role = request.form['role']  # Ambil role dari form
        
        if not username or not password or not nama or not no_telp or not role:
            flash('Please fill in all fields')
            return redirect(url_for('add_user'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, nama, no_telp, level_akses) VALUES (%s, %s, %s, %s, %s)",
                        (username, hashed_password, nama, no_telp, role))
            mysql.connection.commit()
            flash('User added successfully')
            return redirect(url_for('admin_users'))
        except Exception as e:
            flash('Error adding user: ' + str(e))
    
    return render_template('admin/add_user.php')

@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, nama, no_telp, level_akses FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama']
        no_telp = request.form['no_telp']
        role = request.form['role']  # Ambil role dari form
        
        if not username or not nama or not no_telp or not role:
            flash('Please fill in all fields')
            return redirect(url_for('edit_user', id=id))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') if password else user[2]
        
        cur.execute("UPDATE users SET username = %s, password = %s, nama = %s, no_telp = %s, level_akses = %s WHERE id = %s",
                    (username, hashed_password, nama, no_telp, role, id))
        mysql.connection.commit()
        flash('User updated successfully')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.php', user=user)

@app.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('User deleted successfully')
    return redirect(url_for('admin_users'))

# CRUD routes for admin Transaction
from flask import request, Response

@app.route('/admin/transactions')
@login_required
@role_required('admin')
def admin_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM transactions
    """)
    total_transactions = cur.fetchone()[0]

    cur.execute("""
        SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
        FROM transactions
        JOIN users ON transactions.id = users.id
        JOIN products ON transactions.item_type = products.id_products
        ORDER BY transactions.transaction_date DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    transactions = cur.fetchall()

    pagination = {
        'total_pages': ceil(total_transactions / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total_transactions / per_page)
    }

    return render_template('admin/transactions.php', transactions=transactions, pagination=pagination)

@app.route('/admin/transactions/print')
@login_required
@role_required('admin')
def print_transactions():
    print_option = request.args.get('option', 'all')  # Default to 'all' if no option is provided

    cur = mysql.connection.cursor()

    if print_option == 'all':
        # Get all transactions
        cur.execute("""
            SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
            FROM transactions
            JOIN users ON transactions.id = users.id
            JOIN products ON transactions.item_type = products.id_products
            ORDER BY transactions.transaction_date DESC
        """)
    else:
        # Get transactions based on pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        cur.execute("""
            SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
            FROM transactions
            JOIN users ON transactions.id = users.id
            JOIN products ON transactions.item_type = products.id_products
            ORDER BY transactions.transaction_date DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    transactions = cur.fetchall()

    # Create php content for printing
    php_content = render_template('admin/print_transactions.php', transactions=transactions)

    # Return as PDF or php based on request
    if request.args.get('format', '') == 'pdf':
        pdf = pdfkit.from_string(php_content, False)
        response = Response(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=transactions.pdf'
        return response
    else:
        return php_content
# CRUD routes for MANAGER
@app.route('/manager/products')
@login_required
@role_required('manager')
def manager_product():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of products per page
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    total = cur.fetchone()[0]
    cur.execute("SELECT * FROM products LIMIT %s OFFSET %s", (per_page, offset))
    products = cur.fetchall()
    
    pagination = {
        'total_pages': ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total / per_page)
    }

    return render_template('manager/manager_product.php', products=products, pagination=pagination)
# CRUD routes for Package manager
@app.route('/manager/packages')
@login_required
@role_required('manager')
def manager_packages():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM package")
    packages = cur.fetchall()
    return render_template('manager/packages.php', packages=packages)

@app.route('/manager/add_package', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def add_package_m():
    if request.method == 'POST':
        name_package = request.form['name_package']
        total_price = request.form['total_price']
        discount = request.form['discount']

        if 'gambar_packages' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)

        file = request.files['gambar_packages']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/admin/gambarpackages', filename)
            file.save(file_path)

            cur = mysql.connection.cursor()
            try:
                cur.execute("""
                    INSERT INTO package (name_package, total_price, discount, gambar_packages)
                    VALUES (%s, %s, %s, %s)
                """, (name_package, total_price, discount, filename))
                mysql.connection.commit()
                
                flash('Package added successfully')
                return redirect(url_for('manager_packages'))
            except Exception as e:
                flash('Error adding package: ' + str(e))
                mysql.connection.rollback()
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)
    
    return render_template('manager/add_package.php')

@app.route('/manager/packages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def edit_package_m(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM package WHERE id_package = %s", (id,))
    package = cur.fetchone()
    
    if request.method == 'POST':
        name_package = request.form['name_package']
        total_price = request.form['total_price']
        discount = request.form['discount']
        gambar_packages = package[4]  # Keep the old image by default

        if 'gambar_packages' in request.files:
            file = request.files['gambar_packages']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/admin/gambarpackages', filename))
                gambar_packages = filename

        cur.execute("""
            UPDATE package
            SET name_package = %s, total_price = %s, discount = %s, gambar_packages = %s
            WHERE id_package = %s
        """, (name_package, total_price, discount, gambar_packages, id))
        mysql.connection.commit()
        
        flash('Package updated successfully')
        return redirect(url_for('manager_packages'))
    
    package_data = {
        'id_package': package[0],
        'name_package': package[1],
        'total_price': package[2],
        'discount': package[4],
        'gambar_packages': package[3]
    }
    
    return render_template('manager/edit_package.php', package=package_data)

@app.route('/manager/packages/delete/<int:id>', methods=['POST'])
@login_required
@role_required('manager')
def delete_package_m(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM package WHERE id_package = %s", (id,))
    mysql.connection.commit()
    flash('Package deleted successfully')
    return redirect(url_for('manager_packages'))

@app.route('/package_detail/<int:id>', methods=['GET'])
@login_required
def package_detail_m(id):
    cur = mysql.connection.cursor()
    
    # Get package details
    cur.execute("SELECT * FROM package WHERE id_package = %s", (id,))
    package = cur.fetchone()
    
    if not package:
        abort(404)
    
    # Get products associated with the package
    cur.execute("""
        SELECT p.id_products, p.nama_products, p.price, p.gambar_products, pp.quantity
        FROM package_products pp
        JOIN products p ON pp.id_products = p.id_products
        WHERE pp.id_package = %s
    """, (id,))
    products = cur.fetchall()
    
    package_data = {
        'id_package': package[0],
        'name_package': package[1],
        'total_price': package[2],
        'discount': package[4],
        'gambar_package': package[3],
        'products': products
    }
    
    return render_template('package_detail.php', package=package_data)



# CRUD routes for PackageProduct
@app.route('/manager/packages/<int:id>/products')
@login_required
@role_required('manager')
def package_products_m(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT pp.id, p.nama_products, pp.quantity FROM package_products pp JOIN products p ON pp.id_products = p.id_products WHERE pp.id_package = %s", (id,))
    package_products = cur.fetchall()
    return render_template('manager/package_products.php', package_id=id, package_products=package_products)

@app.route('/manager/packages/<int:id>/add_product', methods=['GET', 'POST'])
@login_required
def add_product_to_package_m(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    
    if request.method == 'POST':
        id_products = request.form['id_products']
        quantity = request.form['quantity']
        
        cur.execute("""
            INSERT INTO package_products (id_package, id_products, quantity)
            VALUES (%s, %s, %s)
        """, (id, id_products, quantity))
        mysql.connection.commit()
        
        flash('Product added to package successfully')
        return redirect(url_for('package_products_m', id=id))
    
    return render_template('manager/add_product_to_package.php', package_id=id, products=products)

@app.route('/manager/packages/<int:id>/products/delete/<int:id_products>', methods=['POST'])
@login_required
@role_required('manager')
def delete_product_from_package_m(id, id_products):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM package_products WHERE id = %s", (id_products,))
    mysql.connection.commit()
    flash('Product removed from package successfully')
    return redirect(url_for('package_products_m', id=id))

@app.route('/manager/transactions')
@login_required
@role_required('manager')
def manager_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM transactions
    """)
    total_transactions = cur.fetchone()[0]

    cur.execute("""
        SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
        FROM transactions
        JOIN users ON transactions.id = users.id
        JOIN products ON transactions.item_type = products.id_products
        ORDER BY transactions.transaction_date DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    transactions = cur.fetchall()

    pagination = {
        'total_pages': ceil(total_transactions / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total_transactions / per_page)
    }

    return render_template('manager/transactions.php', transactions=transactions, pagination=pagination)

@app.route('/manager/transactions/print')
@login_required
@role_required('manager')
def print_manager_transactions():
    print_option = request.args.get('option', 'all')  # Default to 'all' if no option is provided

    cur = mysql.connection.cursor()

    if print_option == 'all':
        # Get all transactions
        cur.execute("""
            SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
            FROM transactions
            JOIN users ON transactions.id = users.id
            JOIN products ON transactions.item_type = products.id_products
            ORDER BY transactions.transaction_date DESC
        """)
    else:
        # Get transactions based on pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = 10
        offset = (page - 1) * per_page

        cur.execute("""
            SELECT transactions.id_transactions, users.username, products.nama_products, transactions.quantity, transactions.total_price, transactions.transaction_date
            FROM transactions
            JOIN users ON transactions.id = users.id
            JOIN products ON transactions.item_type = products.id_products
            ORDER BY transactions.transaction_date DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

    transactions = cur.fetchall()

    # Create php content for printing
    php_content = render_template('manager/print_transactions.php', transactions=transactions)

    # Return as PDF or php based on request
    if request.args.get('format', '') == 'pdf':
        pdf = pdfkit.from_string(php_content, False)
        response = Response(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=transactions.pdf'
        return response
    else:
        return php_content
# Print Product
@app.route('/manager/download_manager_products')
@login_required
@role_required('manager')
def download_manager_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_products, nama_products, price, gambar_products, description FROM products")
    products = cur.fetchall()

    # Convert the products data to a DataFrame
    df = pd.DataFrame(products, columns=['ID', 'Nama', 'Price', 'Image', 'Description'])

    # Create an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Products')
        writer.close()

    output.seek(0)

    return send_file(output, download_name='manager_products.xlsx', as_attachment=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manager/orders', methods=['GET'])
@login_required
@role_required('manager')
def manager_orders():
    cur = mysql.connection.cursor()
    
    # Fetch orders with product information
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Count total orders for pagination
    cur.execute("SELECT COUNT(*) FROM orders")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT o.id_orders, p.nama_products, o.quantity, o.status, o.created_at FROM orders o JOIN products p ON o.id_products = p.id_products LIMIT %s OFFSET %s", (per_page, offset))
    orders = cur.fetchall()
    
    # Data for pagination
    pagination = {
        'total_pages': ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total / per_page)
    }
    
    cur.close()
    
    return render_template('manager/manager_orders.html', orders=orders, pagination=pagination)

@app.route('/manager/orders/create', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def create_order():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        id_product = request.form['id_product']
        quantity = request.form['quantity']
        
        cur.execute("INSERT INTO orders (id_products, quantity) VALUES (%s, %s)", (id_product, quantity))
        mysql.connection.commit()
        
        flash('Order created successfully!', 'success')
        return redirect(url_for('manager_orders'))
    
    cur.execute("SELECT id_products, nama_products FROM products")
    products = cur.fetchall()
    
    cur.close()
    
    return render_template('manager/create_order.html', products=products)

    # Ambil data untuk menampilkan daftar orders
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Hitung total orders
    cur.execute("SELECT COUNT(*) FROM orders")
    total = cur.fetchone()[0]
    
    # Ambil data orders dengan informasi produk yang sesuai
    cur.execute("SELECT o.id_orders, o.id_products, p.nama_products, o.quantity, o.status, o.created_at FROM orders o JOIN products p ON o.id_products = p.id_products LIMIT %s OFFSET %s", (per_page, offset))
    orders = cur.fetchall()
    
    # Data untuk pagination
    pagination = {
        'total_pages': ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total / per_page)
    }
    
    cur.close()
    
    try:
        # Ambil daftar produk untuk dropdown
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_products, nama_products FROM products")
        products = cur.fetchall()
        cur.close()
    except MySQLError as e:
        flash(f"Error fetching products: {str(e)}", 'danger')
        products = []
    
    return render_template('manager/manager_orders.html', orders=orders, products=products, pagination=pagination)


@app.route('/manager/orders/update/<int:id_orders>', methods=['GET', 'POST'])
@login_required
@role_required('manager')
def update_order(id_orders):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        id_product = request.form['id_product']
        quantity = request.form['quantity']
        
        cur.execute("UPDATE orders SET id_products=%s, quantity=%s WHERE id_orders=%s", (id_product, quantity, id_orders))
        mysql.connection.commit()
        
        flash('Order updated successfully!', 'success')
        return redirect(url_for('manager_orders'))

    cur.execute("SELECT o.id_orders, o.id_products, o.quantity, o.status, o.created_at, p.nama_products AS product_name FROM orders o JOIN products p ON o.id_products = p.id_products WHERE o.id_orders=%s", (id_orders,))
    order = cur.fetchone()

    cur.execute("SELECT id_products, nama_products FROM products")
    products = cur.fetchall()

    cur.close()

    return render_template('manager/update_order.html', order=order, products=products)



@app.route('/manager/orders/delete/<int:id_orders>', methods=['POST'])
@login_required
@role_required('manager')
def delete_order(id_orders):
    cur = mysql.connection.cursor()
    
    try:
        cur.execute("DELETE FROM orders WHERE id_orders = %s", (id_orders,))
        mysql.connection.commit()
        flash('Order deleted successfully!', 'success')
    except Error as e:
        mysql.connection.rollback()
        flash(f'Error deleting order: {e}', 'danger')
    
    cur.close()
    
    return redirect(url_for('manager_orders'))


# CRUD routes for supplier
@app.route('/supplier')
@login_required
@role_required('supplier')
def supplier():
    
    cur = mysql.connection.cursor()

    # Get total number of products
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # Get total number of transactions
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cur.fetchone()[0]

    # Get total sales amount
    cur.execute("SELECT SUM(total_price) FROM transactions")
    total_sales = cur.fetchone()[0] or 0

    # Get total quantity sold
    cur.execute("SELECT SUM(quantity) FROM transactions")
    total_quantity_sold = cur.fetchone()[0] or 0

    cur.close()

    # Pass the user's name and statistics to the template
    return render_template(
        'supplier/index.php', 
        username=current_user.username, 
        total_products=total_products, 
        total_transactions=total_transactions, 
        total_sales=total_sales, 
        total_quantity_sold=total_quantity_sold
    )
@app.route('/supplier/orders', methods=['GET', 'POST'])
@login_required
@role_required('supplier')
def supplier_orders():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        id_order = request.form['id_order']
        new_status = request.form['status']
        try:
            cur.execute("UPDATE orders SET status = %s WHERE id_orders = %s", (new_status, id_order))
            mysql.connection.commit()
            flash('Order status updated successfully!', 'success')
        except Error as e:
            mysql.connection.rollback()
            flash(f'Error updating order status: {e}', 'danger')
        return redirect(url_for('supplier_orders'))
    
    # Fetch orders with product information
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Count total orders for pagination
    cur.execute("SELECT COUNT(*) FROM orders")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT o.id_orders, p.nama_products, o.quantity, o.status, o.created_at FROM orders o JOIN products p ON o.id_products = p.id_products LIMIT %s OFFSET %s", (per_page, offset))
    orders = cur.fetchall()
    
    # Data for pagination
    pagination = {
        'total_pages': ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total / per_page)
    }
    
    cur.close()
    
    return render_template('supplier/supplier_orders.html', orders=orders, pagination=pagination)
@app.route('/supplier/orders/update_status/<int:id>', methods=['POST'])
@login_required
@role_required('supplier')
def update_order_status(id):
    new_status = request.form['status']
    
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE orders SET status = %s WHERE id_orders = %s", (new_status, id))
            mysql.connection.commit()
            flash('Order status updated successfully!', 'success')
    except Error as e:
        mysql.connection.rollback()
        flash(f'Error updating order status: {e}', 'danger')
    
    return redirect(url_for('supplier_orders'))
# CRUD routes for products
@app.route('/admin/products')
@login_required
@role_required('admin')
def admin_product():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of products per page
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    total = cur.fetchone()[0]
    cur.execute("SELECT * FROM products LIMIT %s OFFSET %s", (per_page, offset))
    products = cur.fetchall()
    
    pagination = {
        'total_pages': ceil(total / per_page),
        'current_page': page,
        'has_prev': page > 1,
        'has_next': page < ceil(total / per_page)
    }

    return render_template('admin/admin_product.php', products=products, pagination=pagination)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_product():
    if request.method == 'POST':
        # Extract form fields
        nama_products = request.form['nama_products']
        price = request.form['price']
        description = request.form['description']
        gambar_products = None  # Initialize to None by default
        
        # Check for the file part in the request
        if 'gambar_products' in request.files:
            file = request.files['gambar_products']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                gambar_products = filename  # Update to new filename
            else:
                flash('Allowed file types are png, jpg, jpeg, gif')
                return redirect(request.url)

        # Ensure all fields are provided
        if not nama_products or not price or not description or not gambar_products:
            flash('Please fill in all fields')
            return redirect(request.url)

        try:
            # Insert product into the database
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO products (nama_products, price, gambar_products, description)
                VALUES (%s, %s, %s, %s)
            """, (nama_products, price, gambar_products, description))
            mysql.connection.commit()

            flash('Product successfully added!')
            return redirect(url_for('admin_product'))
        except Exception as e:
            # Rollback in case of an error
            mysql.connection.rollback()
            flash('Error adding product: ' + str(e))
            return redirect(request.url)
    
    return render_template('admin/add_product.php')


@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id_products = %s", (id,))
    product = cur.fetchone()
    
    if request.method == 'POST':
        nama_products = request.form['nama_products']
        price = request.form['price']
        description = request.form['description']
        gambar_products = product[3]  # Keep the old image by default
        
        # Check if a new file has been uploaded
        if 'gambar_products' in request.files:
            file = request.files['gambar_products']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/admin/gambar_product', filename))
                gambar_products = filename  # Update to new filename
        
        # Update the product details in the database
        cur.execute("""
            UPDATE products
            SET nama_products = %s, price = %s, gambar_products = %s, description = %s
            WHERE id_products = %s
        """, (nama_products, price, gambar_products, description, id))
        mysql.connection.commit()
        
        flash('Product successfully updated!')
        return redirect(url_for('admin_product'))
    
    # Map the product data to a dictionary
    product_data = {
        'id_products': product[0],
        'nama_products': product[1],
        'price': product[2],
        'gambar_products': product[3],
        'description': product[4]
    }
    
    return render_template('admin/edit_product.php', product=product_data)


@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id_products = %s", (id,))
    mysql.connection.commit()
    flash('Product deleted successfully')
    return redirect(url_for('admin_product'))

  # Print Product
@app.route('/admin/download_products')
@login_required
@role_required('admin')
def download_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_products, nama_products, price, gambar_products, description FROM products")
    products = cur.fetchall()

    # Convert the products data to a DataFrame
    df = pd.DataFrame(products, columns=['ID', 'Nama', 'Price', 'Image', 'Description'])

    # Create an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Products')
        writer.close()

    output.seek(0)

    return send_file(output, download_name='products.xlsx', as_attachment=True)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password')
            return redirect(url_for('login'))
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user:
            print(f"User found: {user}")  # Debugging statement
        else:
            print("User not found")  # Debugging statement
        
        if user and bcrypt.check_password_hash(user[2], password):  # Pastikan user[2] adalah kolom password yang benar
            user_obj = User(user[0], user[1], user[5])  # Pastikan user[5] adalah kolom yang valid
            login_user(user_obj)
            print(f"User logged in: {user_obj}")  # Debugging statement
            
            # Redirect berdasarkan peran pengguna
            if user_obj.role == 'admin':
                return redirect(url_for('admin_panel'))
            elif user_obj.role == 'customer':
                return redirect(url_for('produk'))
            elif user_obj.role == 'manager':
                return redirect(url_for('manager'))
            elif user_obj.role == 'supplier':
                return redirect(url_for('supplier'))
            else:
                return redirect(url_for('home'))  # Redirect ke home jika peran tidak dikenal
        
        else:
            flash('Invalid username or password')
            print("Invalid username or password")  # Debugging statement
    
    return render_template('login.php')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nama = request.form.get('nama')
        no_telp = request.form.get('no_telp')
        role = 'customer'  # Default role for new users
        
        if not username or not password or not nama or not no_telp:
            flash('Please fill in all fields')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (username, password, nama, no_telp, level_akses) VALUES (%s, %s, %s, %s, %s)",
                        (username, hashed_password, nama, no_telp, role))
            mysql.connection.commit()
            flash('Registration successful, please login')
            return redirect(url_for('login'))
        except:
            flash('Username already exists')
    
    return render_template('register.php')

# Fungsi asosiasi

# Analisis Data Miningnya
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Route untuk Asosiasi Training
@app.route('/asosiasi', methods=['GET', 'POST'])
def asosiasi():
    if request.method == 'POST':
        model_id = request.form.get('model_id')
        if model_id:
            # Dapatkan model_filename berdasarkan model_id
            cur = mysql.connection.cursor()
            cur.execute("SELECT model_filename FROM model_history WHERE id = %s", (model_id,))
            result = cur.fetchone()
            cur.close()

            if result:
                model_filename = result[0]
                # Muat model dari file
                with open(model_filename, 'rb') as file:
                    model_data = pickle.load(file)
                
                # Kirim data model ke template
                return render_template('manager/asosiasi.html', model_data=model_data, model_history=get_model_history())

    # Jika metode GET atau model_id tidak ditemukan, tampilkan halaman dengan riwayat model
    return render_template('manager/asosiasi.html', model_history=get_model_history())

@app.route('/asosiasi_training', methods=['GET', 'POST'])
def asosiasi_training():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.xlsx'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                
                session['file_path'] = file_path  # Simpan path file dalam session
                
                # Muat data dan dapatkan nama barang unik
                df = pd.read_excel(file_path)
                nama_barang_list = df['Nama Barang'].unique().tolist()
                return render_template('manager/asosiasi_training.html', nama_barang_list=nama_barang_list)
        
        elif 'nama_barang' in request.form:
            nama_barang_list = request.form.getlist('nama_barang')
            min_support = float(request.form['nilai_support'])
            file_path = session.get('file_path')
            
            if file_path:
                model_filename, model_data = train_apriori_model(file_path, nama_barang_list, min_support)
                save_model_history(','.join(nama_barang_list), min_support, model_filename)
                
                flash('Model berhasil dibuat!', 'success')
                return render_template('manager/asosiasi_training.html', model_data=model_data, model_history=get_model_history())
    
    return render_template('manager/asosiasi_training.html', model_history=get_model_history())

@app.route('/delete_model/<int:model_id>', methods=['POST'])
def delete_model(model_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT model_filename FROM model_history WHERE id = %s", (model_id,))
    model_to_delete = cur.fetchone()
    
    # Convert tuple to dictionary
    if model_to_delete:
        column_names = [desc[0] for desc in cur.description]
        model_to_delete_dict = dict(zip(column_names, model_to_delete))

        model_filename = model_to_delete_dict['model_filename']
        if os.path.exists(model_filename):
            os.remove(model_filename)
        
        cur.execute("DELETE FROM model_history WHERE id = %s", (model_id,))
        mysql.connection.commit()
        flash('Model berhasil dihapus!', 'success')
    else:
        flash('Model tidak ditemukan!', 'danger')
    
    return redirect(url_for('asosiasi_training'))


def train_apriori_model(file_path, nama_barang_list, min_support):
    # Muat dan pra-proses data
    df = pd.read_excel(file_path)
    
    # Filter data berdasarkan nama barang yang dipilih
    df_filtered = df[df['Nama Barang'].isin(nama_barang_list)]
    
    # Siapkan data untuk Apriori
    transaksi = df_filtered.groupby('Pelanggan')['Nama Barang'].apply(list).tolist()
    
    # Latih model Apriori
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder
    
    te = TransactionEncoder()
    te_ary = te.fit(transaksi).transform(transaksi)
    df_trans = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df_trans, min_support=min_support, use_colnames=True)
    frequent_itemsets['support_count'] = frequent_itemsets['support'] * len(df_trans)
    
    # Buat aturan asosiasi
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # Simpan model
    model_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"model_apriori_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl")
    model_data = {
        'frequent_itemsets': frequent_itemsets,
        'rules': rules
    }
    with open(model_filename, 'wb') as file:
        pickle.dump(model_data, file)
    
    return model_filename, model_data

def save_model_history(nama_barang, nilai_support, model_filename):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO model_history (nama_barang, nilai_support, model_filename, created_at	
)
        VALUES (%s, %s, %s, %s)
    """, (nama_barang, nilai_support, model_filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mysql.connection.commit()

def get_model_history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM model_history")
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    model_history = [dict(zip(column_names, row)) for row in rows]
    cur.close()
    return model_history
 # Fore casting MA
@app.route('/forecasting_training', methods=['GET', 'POST'])
def forecasting_training():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                
                df = pd.read_csv(file_path)

                # Get the list of product names
                nama_barang_list = df['Nama_Barang'].unique().tolist()
                return render_template('manager/forecasting_training.html', nama_barang_list=nama_barang_list, file=file.filename)

        elif request.form.get('action') == 'train_model':
            nama_barang = request.form.get('nama_barang')
            file = request.form.get('file')
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)

                df = pd.read_csv(file_path)
                df = df[df['Nama_Barang'] == nama_barang]

                df['Moving_Average'] = df['Jumlah_Barang'].rolling(window=3, min_periods=1).mean()
                df['MAE'] = mean_absolute_error(df['Jumlah_Barang'], df['Moving_Average'])

                # Hitung rata-rata jumlah barang dan moving average
                mean_jumlah_barang = df['Jumlah_Barang'].mean()
                mean_moving_average = df['Moving_Average'].mean()

                model_filename = save_forecasting_model(df)
                save_model_to_database(nama_barang, model_filename)
            
                flash('Model berhasil dibuat!', 'success')
                return redirect(url_for('forecasting_training'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nama_barang, model_filename, created_at FROM forecasting_models")
    model_history = cur.fetchall()
    cur.close()

    return render_template('manager/forecasting_training.html', model_history=model_history)

@app.route('/forecasting_results/<int:model_id>', methods=['GET'])
def forecasting_results(model_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT model_filename FROM forecasting_models WHERE id = %s", [model_id])
    result = cur.fetchone()
    cur.close()

    if result:
        model_filename = result[0]
        model_filepath = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
        with open(model_filepath, 'rb') as file:
            model_data = pickle.load(file)

            if not model_data.empty:
                plt.figure(figsize=(10, 6))
                sns.lineplot(data=model_data, x='Tanggal', y='Jumlah_Barang', label='Jumlah Barang')
                sns.lineplot(data=model_data, x='Tanggal', y='Moving_Average', label='Moving Average')
                plt.title('Forecasting Moving Average')
                plt.xlabel('Tanggal')
                plt.ylabel('Jumlah Barang')
                plt.legend()
                plot_filename = f'model_plot_{model_id}.png'
                plot_filepath = os.path.join(app.config['UPLOAD_FOLDER'], plot_filename)
                plt.savefig(plot_filepath)
                plt.close()

                mae = model_data['MAE'].mean()

                return render_template('manager/forecasting_results.html', model_data=model_data, plot_filepath=plot_filename, mae=mae)

    flash('Model tidak ditemukan!', 'danger')
    return redirect(url_for('forecasting_training'))

def save_forecasting_model(dataframe):
    model_filename = f'forecasting_model_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pkl'
    model_filepath = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
    with open(model_filepath, 'wb') as file:
        pickle.dump(dataframe, file)
    return model_filename

def save_model_to_database(nama_barang, model_filename):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO forecasting_models (nama_barang, model_filename, created_at) VALUES (%s, %s, %s)",
                (nama_barang, model_filename, datetime.now()))
    mysql.connection.commit()
    cur.close()



@app.route('/delete_model_forecasting/<int:model_id>', methods=['POST'])
def delete_model_forecasting(model_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM forecasting_models WHERE id = %s", (model_id,))
    mysql.connection.commit()
    cur.close()
    flash('Model berhasil dihapus!', 'success')
    return redirect(url_for('forecasting_training'))


ALLOWED_EXTENSIONS = {'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data(filepath):
    return pd.read_excel(filepath)


def get_products(data):
    product_sales = data.groupby('Nama Barang')['Jumlah Barang'].sum().reset_index()
    product_sales_sorted = product_sales.sort_values(by='Jumlah Barang')
    few_purchased = product_sales_sorted.head(max(1, int(len(product_sales_sorted) * 0.1)))
    often_purchased = product_sales_sorted.tail(max(1, int(len(product_sales_sorted) * 0.1)))
    return few_purchased, often_purchased

@app.route('/forecasting', methods=['GET', 'POST'])
def forecasting():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            data = load_data(filepath)
            few_purchased, often_purchased = get_products(data)
            return render_template('manager/forecasting.html', 
                                   data=data.to_html(), 
                                   few_purchased=few_purchased.to_html(), 
                                   often_purchased=often_purchased.to_html())
    return render_template('manager/forecasting.html')

if __name__ == '__main__':
    app.run(debug=True)
