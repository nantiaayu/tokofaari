{% extends "admin/base_admin.php" %}
{% block content %}
<div class="container mt-4">
    <h1>Packages</h1>
    <a href="{{ url_for('add_package') }}" class="btn btn-primary mb-3">Add Package</a>
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Total Price</th>
                <th>Discount</th>
                <th>Image Packages</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for package in packages %}
                <tr>
                    <td>{{ package[1] }}</td>
                    <td>RP.{{ package[2] }}</td>
                    <td>{{ package[4] }}%</td>
                    <td><img src="{{ url_for('static', filename='admin/gambarpackages/' ~ package[3]) }}" alt="Package Image" class="img-thumbnail" width="100"></td>
                    <td>
                        <a href="{{ url_for('edit_package', id=package[0]) }}" class="btn btn-warning">Edit</a>
                        <form action="{{ url_for('delete_package', id=package[0]) }}" method="post" style="display:inline;">
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                        <a href="{{ url_for('package_products', id=package[0]) }}" class="btn btn-info">Products</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}