import json
import random
import time

class user:
    def __init__(self, id, nome, idade, saldo):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.saldo = saldo

usuarios_cadastrados = []
ids_utilizados = set()

def encontrar_usuario_por_id(id_procurado):
    global usuarios_cadastrados
    usuario: user
    for usuario in usuarios_cadastrados:
        if usuario.id == id_procurado:
            return usuario
    return None

def carregar_usuarios():
    global usuarios_cadastrados, ids_utilizados
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            dados_brutos = json.load(f)
            for dados in dados_brutos:
                novo_usuario = user(dados['id'], dados['nome'], dados['idade'], dados['saldo'])
                usuarios_cadastrados.append(novo_usuario)
                ids_utilizados.add(novo_usuario.id)
    except FileNotFoundError:
        print("O arquivo nao foi encontrado")
        return
    except json.JSONDecodeError:
        print("Arquivo esta vazio ou corrompido")
        return

def salvar_usuarios():
    global usuarios_cadastrados, ids_utilizados
    dados_para_salvar = [usuario.__dict__ for usuario in usuarios_cadastrados]
    try:
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump(dados_para_salvar, f, indent=4)
    except FileNotFoundError:
        print("O arquivo nao foi encontrado")
        return
    except json.JSONDecodeError:
        print("Arquivo esta vazio ou corrompido")
        return
    
def criar_usuario():
    nome = str(input("Digite seu nome: "))
    idade = int(input("Digite sua idade: "))
    saldo = float(input("Digite seu saldo: "))
    novo_id = random.randint(1000,9999)
    global ids_utilizados
    while(novo_id in ids_utilizados):
        novo_id = random.randint(1000,9999)
    novo_usuario = user(id=novo_id, nome=nome, idade=idade, saldo=saldo)
    usuarios_cadastrados.append(novo_usuario)
    ids_utilizados.add(novo_id)
    print(f"Usuario de id {novo_id} criado com sucesso!")
    salvar_usuarios()

def criar_varios_usuarios():
    usuarios_a_serem_cadastrados = int(input("Digite quantos usuarios voce deseja cadastrar: "))
    if usuarios_a_serem_cadastrados <= 0:
        print("ERRO: valor invalido!")
        return
    for i in range(usuarios_a_serem_cadastrados):
        nome = str(input("Digite seu nome: "))
        idade = int(input("Digite sua idade: "))
        saldo = float(input("Digite seu saldo: "))
        novo_id = random.randint(1000,9999)
        global ids_utilizados
        while(novo_id in ids_utilizados):
            novo_id = random.randint(1000,9999)
        novo_usuario = user(id=novo_id, nome=nome, idade=idade, saldo=saldo)
        usuarios_cadastrados.append(novo_usuario)
        ids_utilizados.add(novo_id)
        print(f"Usuario de id {novo_id} criado com sucesso!")
        salvar_usuarios()

def buscar_id():
    global ids_utilizados, usuarios_cadastrados
    user_requisitado: user
    id_requisitado = int(input("Digite o id que voce deseja acessar: "))
    if(id_requisitado in ids_utilizados):
        user_requisitado = encontrar_usuario_por_id(id_requisitado)
        if not user_requisitado:
            return
        if id_requisitado == user_requisitado.id:
            if ("USUARIO EXCLUIDO" == user_requisitado.nome) or (-1 == user_requisitado.idade) or (-1 == user_requisitado.saldo):
                print("ERRO: usuario removido")
                return
            else:
                print(f"Usuario de id {id_requisitado}: {user_requisitado.nome}, {user_requisitado.idade}, {user_requisitado.saldo}.")
                return
    elif(id_requisitado < 1000 or id_requisitado > 9999):
        print("ERRO: valor invalido")
    else:
        print("ERRO: usuario inexistente")
    return

def remover_usuario():
    global ids_utilizados, usuarios_cadastrados
    user_excluido: user
    id_excluido = int(input("Digite o id que voce deseja excluir: "))
    if(id_excluido in ids_utilizados):
        user_excluido = encontrar_usuario_por_id(id_excluido)
        if not user_excluido:
            return
        if user_excluido.nome == "USUARIO EXCLUIDO" or user_excluido.idade == -1 or user_excluido.saldo == -1:
            print("ERRO: usuario removido")
            return
        if id_excluido == user_excluido.id:
            user_excluido.nome = "USUARIO EXCLUIDO"
            user_excluido.idade = -1
            user_excluido.saldo = -1
            salvar_usuarios()
            print("Usuario removido com sucesso!")
    elif(id_excluido < 1000 or id_excluido > 9999):
        print("ERRO: valor invalido")
    else:
        print("ERRO: usuario removido ou inexistente")
    return

def transferencia():
    global usuarios_cadastrados, ids_utilizados
    id1 = int(input("Digite o id que ira transferir: "))
    id2 = int(input("Digite o id que ira receber a transferencia: "))
    usuario1: user
    usuario2: user
    usuario1 = encontrar_usuario_por_id(id1)
    usuario2 = encontrar_usuario_por_id(id2)
    if not usuario2 or not usuario1:
        print("ERRO: Valor invalido para algum dos ids")
        return
    if usuario1.nome == "USUARIO EXCLUIDO" or usuario1.idade == -1 or usuario1.saldo == -1:
        print("ERRO: remetente excluido")
        return
    if usuario2.nome == "USUARIO EXCLUIDO" or usuario2.idade == -1 or usuario2.saldo == -1:
        print("ERRO: destinatario excluido")
        return
    valor = float(input("Digite o valor a ser transferido: "))
    if valor<0 or valor>usuario1.saldo:
        print("ERRO: valor invalido")
        return
    usuario1.saldo -= valor
    usuario2.saldo += valor
    salvar_usuarios()
    print("Transferencia realizada com sucesso!")
    return

def main():
    carregar_usuarios()
    while True:
        print("------- MENU -------")
        print("1- Criar um usuario")
        print("2- Criar varios usuarios")
        print("3- Buscar um usuario por id")
        print("4- Transferir para outro usuario")
        print("5- Remover usuario")
        print("6- Encerrar Sistema")
        print("---------------------")
        selecao = int(input("Escolha uma das opcoes de 1 a 6: "))
        if(selecao == 1):
            criar_usuario()
        elif(selecao == 2):
            criar_varios_usuarios()
        elif(selecao == 3):
            buscar_id()
        elif(selecao == 4):
            transferencia()
        elif(selecao == 5):
            remover_usuario()
        elif(selecao == 6):
            print("Encerrando o sistema...")
            time.sleep(2)
            print("Sistema encerrado")
            break
        else:
            print("ERRO: valor invalido!")
    return 0
if(__name__ == "__main__"):
    main()