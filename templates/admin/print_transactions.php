<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Print Transactions</title>
    <style>
        /* CSS styling for print layout */
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        .page-break {
            page-break-after: always;
        }
        .back-button {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Transactions Report</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Product Name</th>
                <th>Quantity</th>
                <th>Total Price</th>
                <th>Transaction Date</th>
            </tr>
        </thead>
        <tbody>
            {% for transaction in transactions %}
            <tr>
                <td>{{ transaction[0] }}</td>
                <td>{{ transaction[1] }}</td>
                <td>{{ transaction[2] }}</td>
                <td>{{ transaction[3] }}</td>
                <td>RP.{{ transaction[4] }}</td>
                <td>{{ transaction[5] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <button class="back-button" onclick="history.back()">Back</button>
</body>
</html>
