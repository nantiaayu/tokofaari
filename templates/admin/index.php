{% extends "admin/base_admin.php" %}

{% block title %}Dashboard - Admin Panel{% endblock %}

{% block content %}
<h1>Hello, {{ username }}!</h1>
<p>Ini Adalah Informasi Seputar Penjualan</p>

<div class="container mt-4">
    <div class="row">
        <div class="col-md-3">
            <div class="card text-white bg-primary mb-3">
                <div class="card-body">
                    <h5 class="card-title">Total Products</h5>
                    <p class="card-text">{{ total_products }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-success mb-3">
                <div class="card-body">
                    <h5 class="card-title">Total Transactions</h5>
                    <p class="card-text">{{ total_transactions }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-info mb-3">
                <div class="card-body">
                    <h5 class="card-title">Total Sales</h5>
                    <p class="card-text">RP. {{ total_sales }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-white bg-warning mb-3">
                <div class="card-body">
                    <h5 class="card-title">Total Quantity Sold</h5>
                    <p class="card-text">{{ total_quantity_sold }}</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Tambahkan konten lainnya di sini -->
{% endblock %}
