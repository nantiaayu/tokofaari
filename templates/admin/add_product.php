{% extends "admin/base_admin.php" %}

{% block title %}Add Product - Admin Panel{% endblock %}

{% block content %}
<h1>Add Product</h1>
<form method="POST" enctype="multipart/form-data">
    <div class="form-group">
        <label for="nama_products">Nama Product</label>
        <input type="text" class="form-control" id="nama_products" name="nama_products" required>
    </div>
    <div class="form-group">
        <label for="price">Price</label>
        <input type="number" class="form-control" id="price" name="price" step="0.01" required>
    </div>
    <div class="form-group">
        <label for="gambar_products">Gambar Product</label>
        <input type="file" class="form-control" id="gambar_products" name="gambar_products" required>
    </div>
    <div class="form-group">
        <label for="description">Description</label>
        <textarea class="form-control" id="description" name="description" rows="3" required></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Add Product</button>
</form>
{% endblock %}
