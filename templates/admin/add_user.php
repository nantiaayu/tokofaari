{% extends "admin/base_admin.php" %}

{% block title %}Add User - Admin Panel{% endblock %}

{% block content %}
<h1>Add User</h1>
<form method="POST" action="{{ url_for('add_user') }}">
    <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" class="form-control" id="username" name="username" required>
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" name="password" required>
    </div>
    <div class="form-group">
        <label for="nama">Nama:</label>
        <input type="text" class="form-control" id="nama" name="nama" required>
    </div>
    <div class="form-group">
        <label for="no_telp">No. Telp:</label>
        <input type="text" class="form-control" id="no_telp" name="no_telp" required>
    </div>
    <div class="form-group">
        <label for="role">Role:</label>
        <select class="form-control" id="role" name="role" required>
            <option value="admin">Admin</option>
            <option value="customer">Customer</option>
            <option value="manager">manager</option>
            <option value="supplier">supplier</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Add User</button>
</form>
{% endblock %}
