<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Manager{% endblock %}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <style>
        .navbar-dark {
            background: linear-gradient(90deg, #0056b3, #004494);
            color: #fff;
        }
        .navbar-dark .navbar-nav .nav-link {
            color: #fff;
        }
        .navbar-dark .navbar-brand {
            color: #fff;
        }
        .sidebar {
            background: linear-gradient(180deg, #0056b3, #004494);
            height: 100%;
            color: #fff;
            padding: 15px;
        }
        .sidebar .nav-link {
            color: #fff;
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .sidebar .nav-link .fas {
            margin-right: 10px;
        }
        .sidebar .nav-link.active, .sidebar .nav-link:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        .content {
            padding: 20px;
            background-color: #f8f9fa;
            margin-top: 20px;
            margin-right: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            min-height: calc(100vh - 120px); /* Adjust height to fit the footer */
        }
        .footer {
            background: linear-gradient(90deg, #0056b3, #004494);
            color: #fff;
            padding: 10px 0;
            text-align: center;
            position: relative;
            bottom: 0;
            width: 100%;
        }
        .dropdown-menu {
            background-color: #004494;
            color: #fff;
        }
        .dropdown-menu .dropdown-item {
            color: #fff;
        }
        .dropdown-menu .dropdown-item:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <a class="navbar-brand" href="{{ url_for('manager') }}">Manager</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('manager') }}">Dashboard</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('manager_product') }}">Product</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('manager_packages') }}">Manage Packages</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('manager_orders') }}">Manage Orders</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('manager_transactions') }}">Transaction</a>
                </li>
                <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="dropdownMenuButton" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="fas fa-tools"></i> Trained Model
                            </a>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                <a class="dropdown-item" href="{{ url_for('asosiasi_training') }}">Trained Model Asosiasi</a>
                                <a class="dropdown-item" href="{{ url_for('forecasting_training') }}">Trained Model Forecasting</a>
                                <a class="dropdown-item" href="#">History Model</a>
                            </div>
                        </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="">
        <div class="row">
            <div class="col-md-2">
                <div class="sidebar">
                    <ul class="nav flex-column">
                        <li>
                            <h3>Menu Analysis</h3>
                            <hr>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('forecasting') }}">
                                <i class="fas fa-chart-line"></i> Analisis Forecasting
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('asosiasi') }}">
                                <i class="fas fa-boxes"></i> Analisis Stok Barang
                            </a>
                        </li>
                        
                    </ul>
                </div>
            </div>
            <div class="col-md-10">
                <div class="content">
                    {% block content %}
                    {% endblock %}
                </div>
            </div>
        </div>
    </div>
    <footer class="footer">
        <div class="container">
            <span>&copy; 2024 Manager. All rights reserved.</span>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
