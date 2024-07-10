{% extends 'base.php' %}
{% block content %}
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-6">
                <img src="{{ url_for('static', filename='admin/gambar_product/' ~ product['gambar_products']) }}" class="img-fluid" alt="{{ product['nama_products'] }}">
            </div>
            <div class="col-md-6">
                <h1>{{ product['nama_products'] }}</h1>
                <h2>RP.{{ product['price'] }}</h2>
                <p>{{ product['description'] }}</p>
                <form method="POST" action="{{ url_for('transaksi', type='product', id=product['id_products']) }}">
                    <div class="form-group">
                        <label for="quantity">Quantity:</label>
                        <input type="number" class="form-control" id="quantity" name="quantity" min="1" required>
                    </div>
                    <button type="submit" class="btn btn-primary"><i class="fas fa-shopping-cart"></i> Beli</button>
                </form>
            </div>
        </div>
    </div>
{% endblock %}
