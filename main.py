import json
from datetime import datetime
from hashlib import sha256

from flask import Flask, request

from DBHandler import DBHandler
from ResponseModel import ResponseModel

app = Flask(__name__)

PASS = "056210542"

def checkTokenAuth(tokenSHA256Request, USER, route):

    passSHA256 = sha256(PASS.encode('utf-8')).hexdigest()
    minutes = datetime.now().minute

    tokenString = USER + route + passSHA256 + str(minutes)
    tokenSHA256 = sha256(tokenString.encode('utf-8')).hexdigest()

    print(tokenSHA256Request)
    print(tokenSHA256)

    if tokenSHA256 == tokenSHA256Request:
        print('acceso correcto')
        return True
    else:
        print('acceso denegado')
        return False

@app.route('/images', methods=['POST','PUT','DELETE','GET'])
def images():
    print(request.json)
    response = ResponseModel()
    tokenSHA256Request = request.authorization['password']
    user = request.authorization['username']
    route = request.json['route']

    if checkTokenAuth(tokenSHA256Request, user, route):
        try:
            if request.method == 'POST':
                response = addImage(request.json['data'])
            elif request.method == 'GET':
                response = getImages(request.json['data'])
                #response = getProduct(request.json['data'])
            elif request.method == 'PUT':
                pass
                #response = updateProduct(request.json['data'])
            elif request.method == 'DELETE':
                pass
                #response = deleteProduct(request.json['data'])


        except Exception as e:
            print(e)
    else:
        response.data = 'NO TIENES ACCESO'

    return json.dumps(response.__dict__)

def addImage(image):
    response = DBHandler().insertarImagen(image)
    return response

def getImages(_idE):
    response = DBHandler().obtenerImagenes(_idE)
    return response






@app.route('/products', methods=['POST','PUT','DELETE','GET'])
def products():
    print(request.json)
    response = ResponseModel()
    tokenSHA256Request = request.authorization['password']
    user = request.authorization['username']
    route = request.json['route']

    if checkTokenAuth(tokenSHA256Request, user, route):
        try:
            if request.method == 'POST':
                response = addProduct(request.json['data'])
            elif request.method == 'GET':
                response = getProduct(request.json['data'])
            elif request.method == 'PUT':
                response = updateProduct(request.json['data'])
            elif request.method == 'DELETE':
                response = deleteProduct(request.json['data'])


        except Exception as e:
            print(e)
    else:
        response.data = 'NO TIENES ACCESO'

    return json.dumps(response.__dict__)


def deleteProduct(_idE):
    response = DBHandler().eliminarProducto(_idE)
    return response


def updateProduct(producto):
    response = DBHandler().actualizar(producto)
    return response

def getProduct(_idE):
    if _idE == 'all':
        response = DBHandler().obtenerProductos()
    else:
        response = DBHandler().obtenerProductos(_idE)

    return response

def addProduct(producto):
    response = DBHandler().insertarProducto(producto)
    return response





if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')