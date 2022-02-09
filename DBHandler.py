from pymongo import MongoClient

from ResponseModel import ResponseModel


class DBHandler(object):
    def __init__(self):
        self.db = self.connectar()
        self.collection =self.db.get_collection('productos')

    def connectar(self):
        client= MongoClient(
            host='infsalinas.sytes.net:10450',
            serverSelectionTimeoutMS=3000,
            username='2dam03',
            password='056210542',
            authSource='2dam03'
        )
        db= client.get_database('2dam03')
        return db

    def insertarImagen(self, image):
        response = ResponseModel()
        try:
            self.collection = self.db.get_collection('imagenes')
            self.collection.update_one({'_id': image['_id']}, {'$push': {'imagenes': image['imagenes']}}, upsert=True)
            response.resultOk = True
            response.data = 'Imagen insertada con exito'
        except Exception as e:
            print(e)

        return response

    def obtenerImagenes(self, _idE):
        response = ResponseModel()
        try:
            self.collection = self.db.get_collection('imagenes')
            imagenes = self.collection.find_one({'_id': _idE})

            if imagenes is None:
                print("ES NONE")
                response.resultOk = False
                response.data = "No hay imagenes"
            else:
                response.resultOk = True
                response.data = str(imagenes)


        except Exception as e:
            print(e)

        return response

    #######################################
    # PRODUCTOS
    def eliminarProducto(self, _idE):
        response = ResponseModel()

        try:
            self.collection = self.db.get_collection('productos')
            self.collection.delete_one({'_id': _idE})
            response.resultOk = True
            response.data = 'Producto eliminado con exito'
        except Exception as e:
            print(e)

        return response

    def obtenerProducto(self, _idE):
        response = ResponseModel()
        try:
            self.collection = self.db.get_collection('productos')
            producto = self.collection.find_one({'_id': _idE})
            response.resultOk = True
            response.data = str(producto)
        except Exception as e:
            print(e)

        return response

    def actualizar(self, producto):
        response = ResponseModel()
        print(producto['Nombre'])

        try:
            self.collection = self.db.get_collection('productos')
            self.collection.update_one({'_id': producto['_id']}, {'$set': producto})
            response.resultOk = True
            response.data = 'Producto actualizado con exito'
        except Exception as e:
            print(e)

        return response

    # obtenerLista (en los videos)
    def obtenerProductos(self):
        response = ResponseModel()
        try:
            self.collection = self.db.get_collection('productos')
            listaProductos = []
            coleccion = self.collection.find({})
            for producto in coleccion:
                listaProductos.append(producto)

            response.resultOk = True
            response.data = str(listaProductos)

        except Exception as e:
            print(e)

        return response

    def insertarProducto(self, producto):
        response = ResponseModel()
        try:
            self.collection = self.db.get_collection('productos')
            self.collection.insert_one(producto)
            response.resultOk = True
            response.data = 'Producto insertado con exito'
        except Exception as e:
            print(e)

        return response