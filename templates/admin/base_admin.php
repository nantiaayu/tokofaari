<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Admin Panel{% endblock %}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="{{ url_for('admin_panel') }}">Admin Panel</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('admin_panel') }}">Dashboard</a>
                </li>
            <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('admin_users') }}">Manage Users</a>
                </li>
            <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('admin_product') }}">Product</a>
            </li>
            <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin_packages') }}">Manage Packages</a>
                        </li>
                        
            <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('admin_transactions') }}">Transaction</a>
            </li>
                
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-3">
                <div class="sidebar">
                    
                </div>
            </div>
            <div class="col-md-9">
                <div class="content">
                    {% block content %}
                    {% endblock %}
                </div>
            </div>
        </div>
    </div>
    <script src="{{ url_for('static', filename='js/jquery.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
</body>
</html>
