{% extends "admin/base_admin.php" %}

{% block title %}Users - Admin Panel{% endblock %}

{% block content %}
<h1>Manage Users</h1>
<a href="{{ url_for('add_user') }}" class="btn btn-primary">Add User</a>
<table class="table table-bordered mt-3">
    <thead>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Nama</th>
            <th>No. Telp</th>
            <th>Role</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user[0] }}</td>
            <td>{{ user[1] }}</td>
            <td>{{ user[2] }}</td>
            <td>{{ user[3] }}</td>
            <td>{{ user[4] }}</td>
            <td>
                <a href="{{ url_for('edit_user', id=user[0]) }}" class="btn btn-warning">Edit</a>
                <form action="{{ url_for('delete_user', id=user[0]) }}" method="POST" style="display:inline;">
                    <button type="submit" class="btn btn-danger">Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
