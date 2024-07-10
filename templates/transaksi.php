{% extends 'base.php' %}
{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            <img src="{{ url_for('static', filename='admin/gambarproducts/' if type == 'product' else 'admin/gambarpackages/' ) ~ item['gambar'] }}" class="img-fluid" alt="{{ item['name'] }}">
        </div>
        <div class="col-md-6">
            <h1>{{ item['name'] }}</h1>
            <h2>RP.{{ item['price'] }}</h2>
            {% if type == 'package' %}
                <p>Discount: {{ item['discount'] }}%</p>
            {% endif %}
            <p>{{ item['description'] }}</p>
            <form method="POST" action="{{ url_for('transaksi', type=type, id=item['id']) }}">
                <div class="form-group">
                    <label for="quantity">Quantity</label>
                    <input type="number" class="form-control" id="quantity" name="quantity" min="1" value="1" required>
                </div>
                <button type="submit" class="btn btn-primary"><i class="fas fa-shopping-cart"></i> Confirm Purchase</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
