{% extends "admin/base_admin.php" %}
{% block content %}
    <div class="container mt-4">
        <h1>Products in Package</h1>
        <a href="{{ url_for('add_product_to_package', id=package_id) }}" class="btn btn-primary mb-3">Add Product</a>
        <table class="table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for pp in package_products %}
                    <tr>
                        <td>{{ pp[1] }}</td>
                        <td>{{ pp[2] }}</td>
                        <td>
                            <form action="{{ url_for('delete_product_from_package', id=package_id, product_id=pp[0]) }}" method="post" style="display:inline;">
                                <button type="submit" class="btn btn-danger">Remove</button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}
