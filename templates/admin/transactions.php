{% extends "admin/base_admin.php" %}

{% block title %}Transactions - Admin Panel{% endblock %}

{% block content %}
<h1>Transactions</h1>
<div class="d-flex justify-content-between mb-3">
    <div>
        <a href="{{ url_for('print_transactions', option='all', format='html') }}" class="btn btn-primary">Print All</a>
        <a href="{{ url_for('print_transactions', option='page', format='html', page=pagination.current_page) }}" class="btn btn-primary">Print Per Page</a>
    </div>
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <!-- Pagination links -->
        </ul>
    </nav>
</div>
<table class="table table-bordered mt-3">
    <thead>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Total Price</th>
            <th>Transaction Date</th>
        </tr>
    </thead>
    <tbody>
        {% for transaction in transactions %}
        <tr>
            <td>{{ transaction[0] }}</td>
            <td>{{ transaction[1] }}</td>
            <td>{{ transaction[2] }}</td>
            <td>{{ transaction[3] }}</td>
            <td>RP.{{ transaction[4] }}</td>
            <td>{{ transaction[5] }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Pagination links -->
<nav aria-label="Page navigation">
    <ul class="pagination">
        <!-- Pagination links -->
    </ul>
</nav>
{% endblock %}
