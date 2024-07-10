{% extends 'base.php' %}
{% block content %}
<div class="container mt-4">
    <div class="alert alert-success">
        <h4 class="alert-heading">Transaksi Berhasil!</h4>
        <p>Terima kasih telah melakukan pembelian.</p>
        <hr>
        <p class="mb-0">Nama Barang: {{ transaction.name }}</p>
        <p class="mb-0">Jumlah: {{ transaction.quantity }}</p>
        <p class="mb-0">Total Harga: RP.{{ transaction.total_price }}</p>
    </div>
    <a href="{{ url_for('produk') }}" class="btn btn-primary">Continue Shopping</a>
</div>
{% endblock %}
