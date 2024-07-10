{% extends "admin/base_admin.php" %}
{% block content %}
    <div class="container mt-4">
        <h1>Add Product to Package</h1>
        <form method="post" action="{{ url_for('add_product_to_package', id=package_id) }}">
            <div class="form-group">
                <label for="id_products">Product</label>
                <select class="form-control" id="id_products" name="id_products" required>
                    {% for product in products %}
                        <option value="{{ product[0] }}">{{ product[1] }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity</label>
                <input type="number" class="form-control" id="quantity" name="quantity" required>
            </div>
            <button type="submit" class="btn btn-primary">Add Product</button>
        </form>
    </div>
{% endblock %}
