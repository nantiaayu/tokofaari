{% extends "admin/base_admin.php" %}

{% block title %}Edit Product - Admin Panel{% endblock %}

{% block content %}
<h1>Edit Product</h1>
<form action="{{ url_for('edit_product', id=product.id_products) }}" method="POST" enctype="multipart/form-data">
    <div class="form-group">
        <label for="nama_products">Nama Product</label>
        <input type="text" class="form-control" id="nama_products" name="nama_products" value="{{ product.nama_products }}" required>
    </div>
    <div class="form-group">
        <label for="price">Price</label>
        <input type="number" class="form-control" id="price" name="price" step="0.01" value="{{ product.price }}" required>
    </div>
    <div class="form-group">
        <label for="gambar_products">Gambar Product</label>
        <input type="file" class="form-control" id="gambar_products" name="gambar_products">
        {% if product.gambar_products %}
            <p>Current Image: <img src="{{ url_for('static', filename='admin/gambar_product/' ~ product.gambar_products) }}" alt="Current Image" width="100"></p>
        {% endif %}
    </div>
    <div class="form-group">
        <label for="description">Description</label>
        <textarea class="form-control" id="description" name="description" rows="3" required>{{ product.description }}</textarea>
    </div>
    <button type="submit" class="btn btn-primary">Update Product</button>
</form>
{% endblock %}
