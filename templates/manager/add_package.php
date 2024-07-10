{% extends "manager/base_manager.php" %}
{% block content %}
<div class="container mt-4">
    <h1>Add Package</h1>
    <form method="POST" action="{{ url_for('add_package_m') }}" enctype="multipart/form-data">
        <div class="form-group">
            <label for="name_package">Name</label>
            <input type="text" class="form-control" id="name_package" name="name_package" required>
        </div>
        <div class="form-group">
            <label for="total_price">Total Price</label>
            <input type="number" class="form-control" id="total_price" name="total_price" required>
        </div>
        <div class="form-group">
            <label for="discount">Discount</label>
            <input type="number" class="form-control" id="discount" name="discount" required>
        </div>
        <div class="form-group">
            <label for="gambar_packages">Image</label>
            <input type="file" class="form-control-file" id="gambar_packages" name="gambar_packages" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Package</button>
    </form>
</div>
{% endblock %}
