import json
import random
import time

class gereciamento:
    def __init__(self):
        self.usuarios_cadastrados = []
        self.ids_utilizados = set()
        self.mapa_de_usuarios = {}

    def carregar_usuarios(self, filepath = "usuarios_novos.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                dados_brutos = json.load(f)
                for dados in dados_brutos:
                    novo_usuario = user(dados['id'], dados['nome'], dados['idade'], dados['saldo'])
                    novo_usuario.is_active = dados.get('is_active', True)
                    self.usuarios_cadastrados.append(novo_usuario)
                    self.ids_utilizados.add(novo_usuario.id)
                    self.mapa_de_usuarios[novo_usuario.id] = novo_usuario
        except FileNotFoundError:
            print("O arquivo nao foi encontrado. Criando arquivo")
            return None
        except json.JSONDecodeError:
            print("Arquivo esta vazio ou corrompido")
            return None
        pass

    def salvar_usuarios(self, filepath = "usuarios_novos.json"):
        dados_para_salvar = [usuario.__dict__ for usuario in self.usuarios_cadastrados]
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            print("O arquivo nao foi encontrado")
            return
        except json.JSONDecodeError:
            print("Arquivo esta vazio ou corrompido")
            return
        pass

    def encontrar_usuario_por_id(self, id_usuario):
        return self.mapa_de_usuarios.get(id_usuario)
    
    def criar_usuario(self):
        nome = str(input("Digite seu nome: "))
        idade = int(input("Digite sua idade: "))
        saldo = float(input("Digite seu saldo: "))
        novo_id = random.randint(1000,9999)
        while(novo_id in self.ids_utilizados):
            novo_id = random.randint(1000,9999)
        novo_usuario = user(id=novo_id, nome=nome, idade=idade, saldo=saldo)
        self.usuarios_cadastrados.append(novo_usuario)
        self.mapa_de_usuarios[novo_usuario.id] = novo_usuario
        self.ids_utilizados.add(novo_id)
        print(f"Usuario de id {novo_id} criado com sucesso!")
        self.salvar_usuarios()

class user:
    def __init__(self, id, nome, idade, saldo):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.saldo = saldo
        self.is_active = True

    def acessar_informacoes(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Saldo: {self.saldo}")

    def transferencia(self, id2, valor, banco:gereciamento):
        usuario2 = banco.encontrar_usuario_por_id(id2)
        if not usuario2:
            print("ERRO: Valor invalido para algum dos ids")
            return
        if usuario2.is_active == False:
            print("ERRO: destinatario excluido")
            return
        if valor<0 or valor>self.saldo:
            print("ERRO: valor invalido")
            return
        self.saldo -= valor
        usuario2.saldo += valor
        banco.salvar_usuarios()
        print("Transferencia realizada com sucesso!")
        return
    
    def remover_seu_usuario(self, banco:gereciamento):
        self.is_active = False
        print("Usuario removido com sucesso!")
        banco.salvar_usuarios()
                
    
class admin:
    def __init__(self):
        pass

    def busca_de_id(self, id_requisitado, banco:gereciamento):
        user_requisitado: user
        if(id_requisitado in banco.ids_utilizados):
            user_requisitado = banco.encontrar_usuario_por_id(id_requisitado)
            if not user_requisitado:
                print("ERRO: usuario inexistente")
            if id_requisitado == user_requisitado.id:
                if (user_requisitado.is_active == False):
                    print("ERRO: usuario removido")
                else:
                    print(f"Usuario de id {id_requisitado}: {user_requisitado.nome}, {user_requisitado.idade}, {user_requisitado.saldo}.")
        elif(id_requisitado < 1000 or id_requisitado > 9999):
            print("ERRO: valor invalido")
        else:
            print("ERRO: usuario inexistente")

    def remocao_de_usuario(self, id_excluido, banco:gereciamento):
        user_excluido: user
        if(id_excluido in banco.ids_utilizados):
            user_excluido = gereciamento.encontrar_usuario_por_id(id_excluido)
            if not user_excluido:
                return
            if (user_excluido.is_active == False):
                print("ERRO: usuario removido")
                return
            if (id_excluido == user_excluido.id):
                user_excluido.is_active = False
                banco.mapa_de_usuarios.update(user_excluido.nome, user_excluido.idade, user_excluido.saldo)
                gereciamento.salvar_usuarios()
                print("Usuario removido com sucesso!")
        elif(id_excluido < 1000 or id_excluido > 9999):
            print("ERRO: valor invalido")
        else:
            print("ERRO: usuario removido ou inexistente")
        return

def main():
    Banco = gereciamento()
    Banco.carregar_usuarios()
    estado = int(input("Digite [1] se voce ainda nao possui uma conta, [2] para acessar o menu de usuario ou [3] caso voce seja um administrador: "))
    if(estado == 1):
        print("Acessando a criacao de usuario...")
        time.sleep(2)
        Banco.criar_usuario()
        print("Usuario criado com sucesso")
        return 0
    elif(estado == 2):
        id_logado = int(input("Digite seu id: "))
        usuario_conectado: user
        usuario_conectado = Banco.encontrar_usuario_por_id(id_logado)
        if not id_logado or usuario_conectado.is_active == False:
            print("ERRO: Usuario nao existente")
        else:
            while True:
                print("------- MENU -------")
                print("1- Acessar suas informacoes")
                print("2- Transferir para outro usuario")
                print("3- Excluir seu usuario")
                print("4- Encerrar Sistema")
                print("---------------------")
                selecao2 = int(input("Escolha uma das opcoes de 1 a 4: "))
                if(selecao2 == 1):
                    usuario_conectado.acessar_informacoes()
                elif(selecao2 == 2):
                    id2 = int(input("Digite o id que ira receber a transferencia: "))
                    valor = float(input("Digite o valor a ser transferido: "))
                    usuario_conectado.transferencia(id2, valor)
                elif(selecao2 == 3):
                    confirmacao = int(input("Tem certeza que deseja excluir seu usuario(1- Sim/ 0- Nao)? Obs:Ele nao podera ser restaurado."))
                    if confirmacao == 1:
                        usuario_conectado.remover_seu_usuario(Banco)
                        break
                    elif confirmacao == 0:
                        continue
                    else: 
                        print("ERRO: valor invalido!")
                        continue
                elif(selecao2 == 4):
                    print("Encerrando o sistema...")
                    time.sleep(2)
                    print("Sistema encerrado")
                    break
                else:
                    print("ERRO: valor invalido!")
            return 0
    elif(estado == 3):
        senha = str(input("Digite a senha de administrador: "))
        if(senha == "senha1234"):
            administrador_logado = admin()
            while(True):
                print("Bem vindo!")
                print("------- MENU -------")
                print("1- Buscar um usuario")
                print("2- Remover usuario")
                print("3- Encerrar Sistema")
                print("---------------------")
                selecao3 = int(input("Escolha uma das opcoes de 1 a 3:"))
                if(selecao3 == 1):
                    id_desejado = int(input("Digite o id desejado: "))
                    administrador_logado.busca_de_id(id_desejado, Banco)
                elif(selecao3 == 2):
                    id_a_ser_excluido = int(input("Digite o id a ser excluido: "))
                    administrador_logado.remocao_de_usuario(id_a_ser_excluido, Banco)
                elif(selecao3 == 3):
                    print("Encerrando o sistema...")
                    time.sleep(2)
                    print("Sistema encerrado")
                    break
                else:
                    print("ERRO: valor invalido!")
        else:
            print("Senha incorreta!")
        return 0
if(__name__ == "__main__"):
    main()