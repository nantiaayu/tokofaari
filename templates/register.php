{% extends "base.php" %}

{% block content %}
<h1>Register</h1>
<form method="post">
    <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" class="form-control" required>
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" class="form-control" required>
    </div>
    <div class="form-group">
        <label for="nama">Nama:</label>
        <input type="text" id="nama" name="nama" class="form-control" required>
    </div>
    <div class="form-group">
        <label for="no_telp">No. Telp:</label>
        <input type="text" id="no_telp" name="no_telp" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary">Register</button>
</form>
{% endblock %}
