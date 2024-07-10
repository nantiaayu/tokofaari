{% extends 'base.php' %}
{% block content %}
    <div class="container mt-4">
        <h1>Purchase History</h1>
        {% if transactions %}
            <table class="table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Total Price</th>
                        <th>Purchase Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for transaction in transactions %}
                        <tr>
                            <td>{{ transaction[1] }}</td>
                            <td>{{ transaction[2] }}</td>
                            <td>RP.{{ transaction[3] }}</td>
                            <td>{{ transaction[4] }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p>You have not made any purchases yet.</p>
        {% endif %}
    </div>
{% endblock %}
