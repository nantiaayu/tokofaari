{% extends 'base.php' %}
{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            <img src="{{ url_for('static', filename='admin/gambarpackages/' ~ package['gambar_package']) }}" class="img-fluid" alt="{{ package['name_package'] }}">
        </div>
        <div class="col-md-6">
            <h1>{{ package['name_package'] }}</h1>
            <h2>RP.{{ package['total_price'] }}</h2>
            <p>Discount: {{ package['discount'] }}%</p>
            <h3>Included Products</h3>
            <ul>
                {% for product in package['products'] %}
                <li>{{ product[1] }} - Quantity: {{ product[4] }}</li>
                {% endfor %}
            </ul>
            <form method="POST" action="{{ url_for('transaksi', type='package', id=package['id_package']) }}">
                <div class="form-group">
                    <label for="quantity">Quantity</label>
                    <input type="number" class="form-control" id="quantity" name="quantity" min="1" value="1" required>
                </div>
                <button type="submit" class="btn btn-primary"><i class="fas fa-shopping-cart"></i> Beli</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
