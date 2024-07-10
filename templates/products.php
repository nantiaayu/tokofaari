{% extends 'base.php' %}
{% block content %}
<h1>Paket Products</h1>

<div class="container mx-auto mt-4">
    <div class="row">
        {% for package in packages %}
        <div class="col-md-4">
            <div class="card" style="width: 18rem;">
                <img src="{{ url_for('static', filename='admin/gambarpackages/' ~ package[3]) }}" class="card-img-top" alt="Package Image">
                <div class="card-body">
                    <h5 class="card-title">{{ package[1] }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">RP.{{ package[2] }}</h6>
                    <p class="card-text">Discount: {{ package[4] }}%</p>
                    <a href="{{ url_for('package_detail', id=package[0]) }}" class="btn mr-2"><i class="fas fa-link"></i> Beli</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- Pagination for Packages -->
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if pagination_packages.has_prev %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('produk', page_packages=pagination_packages.current_page - 1, page_products=pagination_products.current_page) }}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </span>
        </li>
        {% endif %}
        
        {% for p in range(1, pagination_packages.total_pages + 1) %}
        <li class="page-item {% if p == pagination_packages.current_page %}active{% endif %}">
            <a class="page-link" href="{{ url_for('produk', page_packages=p, page_products=pagination_products.current_page) }}">{{ p }}</a>
        </li>
        {% endfor %}
        
        {% if pagination_packages.has_next %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('produk', page_packages=pagination_packages.current_page + 1, page_products=pagination_products.current_page) }}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </span>
        </li>
        {% endif %}
    </ul>
</nav>

<h1>Products</h1>

<div class="container mx-auto mt-4">
    <div class="row">
        {% for product in products %}
        <div class="col-md-4">
            <div class="card" style="width: 18rem;">
                <img src="{{ url_for('static', filename='admin/gambar_product/' ~ product[3]) }}" class="card-img-top" alt="...">
                <div class="card-body">
                    <h5 class="card-title">{{ product[1] }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">RP.{{ product[2] }}</h6>
                    <p class="card-text">Deskripsi: {{ product[4] }}</p>
                    <a href="{{ url_for('produk_detail', id=product[0]) }}" class="btn mr-2"><i class="fas fa-link"></i> Beli</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<!-- Pagination for Products -->
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if pagination_products.has_prev %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('produk', page_packages=pagination_packages.current_page, page_products=pagination_products.current_page - 1) }}" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                <span class="sr-only">Previous</span>
            </span>
        </li>
        {% endif %}
        
        {% for p in range(1, pagination_products.total_pages + 1) %}
        <li class="page-item {% if p == pagination_products.current_page %}active{% endif %}">
            <a class="page-link" href="{{ url_for('produk', page_packages=pagination_packages.current_page, page_products=p) }}">{{ p }}</a>
        </li>
        {% endfor %}
        
        {% if pagination_products.has_next %}
        <li class="page-item">
            <a class="page-link" href="{{ url_for('produk', page_packages=pagination_packages.current_page, page_products=pagination_products.current_page + 1) }}" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </a>
        </li>
        {% else %}
        <li class="page-item disabled">
            <span class="page-link" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                <span class="sr-only">Next</span>
            </span>
        </li>
        {% endif %}
    </ul>
</nav>

{% endblock %}
