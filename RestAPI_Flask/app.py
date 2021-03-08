from flask import Flask, request, abort
from sqlalchemy import create_engine
import base64

engine = create_engine('postgresql://postgres:postgres@localhost:5432/teste_API', echo=True)

app = Flask(__name__)
app.secret_key = 'teste-api'
def inserePaciente(cod_paciente,nome, sexo):
    engine.execute("INSERT INTO paciente (cod_paciente, nome, sexo) VALUES("+str(cod_paciente)+", '"+nome+"', '"+sexo+"')")

def inserePedido(cod_pedido, ordem_servico,cod_paciente):
    engine.execute("INSERT INTO pedido(cod_pedido,ordem_servico,cod_paciente) VALUES('" + cod_pedido + "', " + str(ordem_servico) + ", '" + str(cod_paciente) + "')")

def inserePedidoExame(ordem_servico,cod_exame):
    engine.execute("INSERT INTO pedido_exame(ordem_servico,cod_exame) VALUES(" + str(ordem_servico) + ", " + str(cod_exame) + ")")


@app.route('/api/pedidoExame', methods=['POST'])
def recebePedido():
    if not request.json or not 'identificador' in request.json:
        abort(400)
    parametro = request.get_json()
    print(parametro)
    chave = parametro["identificador"] + str(parametro["Pedido"]["OrdemServico"])
    chave_bytes = chave.encode('ascii')
    chave_base = base64.b64encode(chave_bytes)
    base64_message = chave_base.decode('ascii')

    if base64_message != str(parametro["Pedido"]["Codigo"]):
        return {'codigo' : 1 ,'mensagem': 'Código do pedido não correponde a chave correta.'}

    result = engine.execute("select count(*) qtd from paciente where cod_paciente = '"+str(parametro["Paciente"]["Codigo"])+"'")
    for row in result:
        if row['qtd'] == 0:
            inserePaciente(parametro["Paciente"]["Codigo"],parametro["Paciente"]["Nome"],parametro["Paciente"]["Sexo"])

    result = engine.execute("select count(*) qtd from pedido where ordem_servico = " + str(parametro["Pedido"]["OrdemServico"]) )
    for row in result:
        if row['qtd'] == 0:
            inserePedido(parametro["Pedido"]["Codigo"], parametro["Pedido"]["OrdemServico"],
                           parametro["Paciente"]["Codigo"])

            for exame in parametro['Exames']['Exame']:
                inserePedidoExame(parametro["Pedido"]["OrdemServico"],exame["Codigo"])
        else:
            return {'codigo' : 1 ,'mensagem': 'Número de ordem de serviço já existe.'}

    return { 'codigo' : 0, 'mensagem' : 'Pedido de exame gravado com sucesso!'}

app.run(debug=True)