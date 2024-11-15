from flask import Blueprint, render_template,request
from database.models.cliente import Cliente
from flask import jsonify
import asyncio
import asyncpg

cliente_route = Blueprint('cliente',__name__)

'''
rota de cliente
    -/clientes/ (GET)-listar clientes
    -clientes/(POST) - inserir cliente no servidor
    -clientes/new (GET)- renderizar o form para criar clientes
    -/clientes/<id> (GET)-obter dados de um cliente
    -/clientes/<id>/edit (GET) - renderizar um form para editar um cliente
    -/clientes/<id>/update (PUT)- atualiza os dados do cliente
    -/clientes/<id>/delete (DELETE) - deleta usuario
'''


@cliente_route.route('/')
def lista_clientes():
    clientes = Cliente.select()
    lista_cliente = []
    for cliente in clientes:
        cliente_data = {
        'id':cliente.id,
        'nome':cliente.nome,
        'email':cliente.email,
        }
        lista_cliente.append(cliente_data)
    return lista_cliente
    # return jsonify(lista_cliente)



@cliente_route.route('/', methods=['POST'])
def inserir_cliente():
    data = request.json

    clientes = Cliente.select()
    queries = clientes.where(Cliente.email == data['email'])

    for clente in queries:
        if(clente):
            return {"status": "Email ja cadastrado!"},404
    

    novo_usuario =Cliente.create(
        nome = data['nome'],
        email = data['email'],        
        )
    
    cliente_data = {
        'nome':novo_usuario.nome,
        'email':novo_usuario.email,
        }
    
    return jsonify(cliente_data)
        
    


@cliente_route.route('/<int:cliente_id>')
def detalhe_cliente(cliente_id):
    cliente = Cliente.get_by_id(cliente_id)
    cliente_data = {
        'id':cliente.id,
        'nome':cliente.nome,
        'email':cliente.email,

    }
    return jsonify(cliente_data)



@cliente_route.route('/<int:cliente_id>/update', methods=['PUT'])
def atualizar_cliente(cliente_id):
    data = request.get_json()

    cliente_editado = Cliente.get_by_id(cliente_id)
    cliente_editado.nome = data['nome']
    cliente_editado.email = data['email']
    cliente_editado.save()

    cliente_data = {
        'id':cliente_editado.id,
        'nome':cliente_editado.nome,
        'email':cliente_editado.email,

    }
    return jsonify(cliente_data)


@cliente_route.route('/<int:cliente_id>/update', methods=['PATCH'])
def atualizar_campo_cliente(cliente_id):
    data = request.get_json()

    cliente_editado = Cliente.get_by_id(cliente_id)
    cliente_editado.nome = data.get('nome', cliente_editado.nome)
    cliente_editado.email = data.get('email', cliente_editado.email)
    cliente_editado.save()

    cliente_data = {
        'id':cliente_editado.id,
        'nome':cliente_editado.nome,
        'email':cliente_editado.email,

    }
    return jsonify(cliente_data)
    
    

@cliente_route.route('/<int:cliente_id>/delete', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = Cliente.get_by_id(cliente_id)
    cliente.delete_instance()
    return{"deleted":"ok"}