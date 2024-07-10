{% extends "admin/base_admin.php" %}
{% block content %}
<div class="container mt-4">
    <h1>Edit Package</h1>
    <form method="POST" action="{{ url_for('edit_package', id=package['id_package']) }}" enctype="multipart/form-data">
        <div class="form-group">
            <label for="name_package">Name</label>
            <input type="text" class="form-control" id="name_package" name="name_package" value="{{ package['name_package'] }}" required>
        </div>
        <div class="form-group">
            <label for="total_price">Total Price</label>
            <input type="number" class="form-control" id="total_price" name="total_price" value="{{ package['total_price'] }}" required>
        </div>
        <div class="form-group">
            <label for="discount">Discount</label>
            <input type="number" class="form-control" id="discount" name="discount" value="{{ package['discount'] }}" required>
        </div>
        <div class="form-group">
            <label for="gambar_packages">Image</label>
            <input type="file" class="form-control-file" id="gambar_packages" name="gambar_packages">
            {% if package['gambar_packages'] %}
            <img src="{{ url_for('static', filename='admin/gambarpackages/' ~ package['gambar_packages']) }}" alt="Package Image" class="img-thumbnail mt-2" width="150">
            {% endif %}
        </div>
        <button type="submit" class="btn btn-primary">Update Package</button>
    </form>
</div>
{% endblock %}
