{% extends "admin/base_admin.php" %}

{% block title %}Edit User - Admin Panel{% endblock %}

{% block content %}
<h1>Edit User</h1>
<form method="POST" action="{{ url_for('edit_user', id=user[0]) }}">
    <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" class="form-control" id="username" name="username" value="{{ user[1] }}" required>
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" name="password">
    </div>
    <div class="form-group">
        <label for="nama">Nama:</label>
        <input type="text" class="form-control" id="nama" name="nama" value="{{ user[2] }}" required>
    </div>
    <div class="form-group">
        <label for="no_telp">No. Telp:</label>
        <input type="text" class="form-control" id="no_telp" name="no_telp" value="{{ user[3] }}" required>
    </div>
    <div class="form-group">
        <label for="role">Role:</label>
        <select class="form-control" id="role" name="role" required>
            <option value="admin" {% if user[4] == 'admin' %}selected{% endif %}>Admin</option>
            <option value="customer" {% if user[4] == 'customer' %}selected{% endif %}>Customer</option>
            <option value="manager" {% if user[4] == 'manager' %}selected{% endif %}>Manager</option>
            <option value="supplier" {% if user[4] == 'supplier' %}selected{% endif %}>Supplier</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Update User</button>
</form>
{% endblock %}
