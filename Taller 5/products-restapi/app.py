import json
import re
from django.dispatch import receiver
from flask import Flask, jsonify, request
from soupsieve import match

app = Flask(__name__)

from products import products
from seller import seller
from customer import customer
from stockProducts import stock
from recommendation import productsSold

from neo4j import GraphDatabase

graphdb = GraphDatabase.driver(uri= "bolt://localhost:7687",auth=("RedSocial","12345"))

print(graphdb)

session = graphdb.session()

#q1 = " MATCH (a:Vendedor {nombre:'Jesus Barrios'}) RETURN a "  
#nodes = session.run(q1)
#for node in nodes:
    #print(node)


@app.route('/products')
def getProducts():
    return jsonify({"products" : products})

@app.route('/seller')
def getSeller():
    return jsonify({"seller": seller})

@app.route('/customer')
def getCustomer():
    return jsonify({"customer": customer})

@app.route('/stockProducts')
def getStockProducts():
    return jsonify({"stockProducts": stock})

@app.route('/recommendation')
def getRecommendation():
    return jsonify({"recommendation": productsSold})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if(len(productsFound) > 0):
        return jsonify({"product":productsFound[0]})
    return jsonify({"message":"Product not found"})

@app.route('/products/rating')
def getRating():
    productsTop = [product for product in products if product['rating'] > 3]
    if(len(productsTop) > 0):
        products.append(productsTop)
        return jsonify({"product":productsTop})
    return jsonify({"message":"Product not found"})


@app.route('/recommendation', methods=['POST'])
def addRecommendation():
    new_recommendation = {
        "name" : request.json['name'],
        "rating" : request.json['rating'],
        "stockSold" : request.json['stockSold']
    }


@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message": "Product added Succesfully","products": products})


@app.route('/seller', methods=['POST'])
def addSeller():
    new_Seller = {
        "name": request.json['name'],
        "ID": request.json['ID'],
        "Name of products sold": request.json['Name of products sold']
    }
    seller.append(new_Seller)
    return jsonify({"message": "Seller added Succesfully","seller": seller})


@app.route('/customer', methods=['POST'])
def addCustomer():
    new_Customer = {
        "name": request.json['name'],
        "ID": request.json['ID'],
        "quantity_sold": request.json['quantity_sold'],
        "product sold": request.json ['product sold']
    }
    customer.append(new_Customer)
    return jsonify({"message": "Customer added Succesfully","customer": customer})


if __name__ == '__main__':
    app.run(debug = True, port = 4000)