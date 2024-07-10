{% extends 'base.html' %}
{% block content %}
<div class="card">
    <div class="card-body">
        <h5 class="card-title">Profil Pengguna</h5>
        <p><strong>ID:</strong> {{ current_user.id }}</p>
        <p><strong>Username:</strong> {{ current_user.username }}</p>
        <p><strong>Nama:</strong> {{ current_user.nama }}</p>
        <p><strong>No Telp:</strong> {{ current_user.no_telp }}</p>
        <p><strong>Level Akses:</strong> {{ current_user.level_akses }}</p>
    </div>
</div>
{% endblock %}
