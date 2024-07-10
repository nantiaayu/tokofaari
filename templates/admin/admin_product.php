{% extends "admin/base_admin.php" %}

{% block title %}Product - Admin Panel{% endblock %}

{% block content %}
<h1>Products</h1>
<a href="{{ url_for('add_product') }}" class="btn btn-primary">Add Product</a>
<a href="{{ url_for('download_products') }}" class="btn btn-secondary">Download Excel</a>
<table class="table table-bordered mt-3">
    <thead>
        <tr>
            <th>ID</th>
            <th>Nama</th>
            <th>Price</th>
            <th>Gambar</th>
            <th>Description</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for product in products %}
        <tr>
            <td>{{ product[0] }}</td>
            <td>{{ product[1] }}</td>
            <td>{{ product[2] }}</td>
            <td>
                {% if product[3] %}
                    <img src="{{ url_for('static', filename='admin/gambar_product/' ~ product[3]) }}" alt="Product Image" style="max-width: 100px;">
                {% else %}
                    No Image
                {% endif %}
            </td>
            <td>{{ product[4] }}</td>
            <td>
                <a href="{{ url_for('edit_product', id=product[0]) }}" class="btn btn-warning">Edit</a>
                <form action="{{ url_for('delete_product', id=product[0]) }}" method="POST" style="display:inline;">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if pagination.has_prev %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('admin_product', page=pagination.current_page - 1) }}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </span>
        </li>
        {% endif %}
        
        {% for p in range(1, pagination.total_pages + 1) %}
        <li class="page-item {% if p == pagination.current_page %}active{% endif %}">
            <a class="page-link" href="{{ url_for('admin_product', page=p) }}">{{ p }}</a>
        </li>
        {% endfor %}
        
        {% if pagination.has_next %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('admin_product', page=pagination.current_page + 1) }}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </span>
        </li>
        {% endif %}
    </ul>
</nav>
{% endblock %}
