# Updated Flask App

from flask import Flask, render_template, jsonify
import psycopg2
import json
import ssl
from werkzeug.serving import run_simple

app = Flask(__name__)

# Replace these values with your PostgreSQL connection details
DB_HOST = "localhost"
DB_NAME = "kuwasaDB"
DB_USER = "nact"
DB_PASSWORD = "nact"


# Path to your SSL certificate and private key files (replace with your actual files)
SSL_CERT = 'certificate.crt'
SSL_KEY = 'private.key'

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(SSL_CERT, SSL_KEY)

@app.route('/')
def index():
    connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customername, accountnumber, controlnumber, meternumber, mobilenumber, house_number, zonename, routename, resident_type,street_name,
            ST_Y(ST_Transform(geom, 4326)) AS latitude_column,  
            ST_X(ST_Transform(geom, 4326)) AS longitude_column
        FROM gis.customers_debts_with_id;
    """)
    customers = cursor.fetchall()

    connection.close()

    # Convert the customer data to a list of dictionaries
    customer_list = [{
        'customername': customer[0],
        'accountnumber': customer[1],
        'controlnumber': customer[2],
        'meternumber': customer[3],
        'mobilenumber': customer[4],
        'house_number': customer[5],
        'zonename': customer[6],
        'routename': customer[7],
        'resident_type': customer[8],
		'street_name': customer[9],
        'latitude': float(customer[10]) if customer[10] is not None else None,
        'longitude': float(customer[11]) if customer[11] is not None else None,
    } for customer in customers]

    # Use json.dumps to serialize the customer data
    customers_json = json.dumps(customer_list)

    return render_template('index.html', customers_json=customers_json)

@app.route('/customer/<account_number>')
def customer_details(account_number):
    connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = connection.cursor()

    query = """
        SELECT customername, accountnumber, controlnumber, meternumber, mobilenumber, house_number, zonename, routename, resident_type,street_name,
            ST_Y(ST_Transform(geom, 4326)) AS latitude_column,  
            ST_X(ST_Transform(geom, 4326)) AS longitude_column 
        FROM gis.customers_debts_with_id
        WHERE accountnumber = %s;
    """
    cursor.execute(query, (account_number,))

    customer = cursor.fetchone()

    connection.close()

    return render_template('customer_details.html', customer=customer)

if __name__ == '__main__':
    # Run the app with SSL support using werkzeug server
    run_simple('0.0.0.0', 8000, app, ssl_context=context, use_reloader=True, use_debugger=True)

