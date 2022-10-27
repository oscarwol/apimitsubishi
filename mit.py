from ast import Try
from ipaddress import ip_address
import re
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
url = "mysql+pymysql://devops:D3vops-2022@3.133.84.181:3306/mitsubishi"
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
base = db.Model.metadata.reflect(db.engine)
#print(db.Model.metadata.tables)

host = ""


class test_drive_users(db.Model):
    __table__ = db.Model.metadata.tables["test_drive"]
    
    def __init__(self, nombre, apellido, telefono, correo, modelo,  concesionario, ip_address, estado):
        self.nombre =  nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.modelo = modelo
        self.concesionario = concesionario
        self.ip_address = ip_address
        self.estado = estado


class test_drive_users_Schema(ma.Schema):
    class Meta:
        fields = ('id','nombre', 'apellido', 'telefono', 'correo', 'modelo',  'concesionario', 'ip_address', 'fecha_registro', 'estado')
        
test_drive_users_schema = test_drive_users_Schema()
test_drive_users_schemas = test_drive_users_Schema(many=True)


@app.route(host+'/')
def index():
    return {"API": "Mitsibishi"}


@app.route(host+'/newuser', methods=['POST'])
def nuevo_usuario():
    if True:
        nombre = re.sub(r"[^A-Za-z-ÁáÉéÍíÓóÚú ]+", "",  request.json['nombre']).upper()
        apellido = re.sub(r"[^A-Za-z-ÁáÉéÍíÓóÚú ]+", "",  request.json['apellido']).upper()
        correo = request.json['correo']
        telefono = request.json['telefono']
        modelo = request.json['modelo']
        concesionario = request.json['concesionario']
        estado = 1
        ip_address = 0
             
        nuevo_test_drive = test_drive_users(nombre,apellido,telefono,correo,modelo,concesionario,ip_address,estado)

        db.session.add(nuevo_test_drive)
        db.session.commit()


        return {"Exitoso": 201}
    #except:
        #return 'No hay resultados',404



@app.route(host+'/users', methods=['GET'])
def get_archivos():
    files = test_drive_users.query.all()
    if files:
        return test_drive_users_schemas.jsonify(files),200
    return 'No hay resultados',404


if __name__ == "__main__":
    app.run()
    