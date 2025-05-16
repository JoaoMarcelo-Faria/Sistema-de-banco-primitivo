import random
import re
import unidecode

palavra_comp: str
palavra_user: str
usadas: list = []
arquivo = r"C:\Codigos\projetos\palavras.txt"
try:
    with open(arquivo, "r", encoding="utf-8") as f:
        texto = f.read()
    palavras = texto.split()
    palavra_comp = random.choice(palavras)
    tamanho = len(palavra_comp) 
except FileNotFoundError:
    print(f"O arquivo '{arquivo}' não foi encontrado.")
    
while(tamanho>6):
        palavra_comp = random.choice(palavras)
        tamanho = len(palavra_comp)
palavra_comp = unidecode.unidecode(palavra_comp)
palavra_comp = re.sub(r'[^a-z\s]', '', palavra_comp)


palavra_user = input(f"Digite uma palavra de {tamanho} caracteres minusculos:")
tentativas = 1
while(tentativas<=5):
    if len(palavra_user) != tamanho:
        print(f"Erro: sua palavra deve ter {tamanho} caracteres.")
        palavra_user = input("Tente de novo.")
        tentativas = tentativas + 1
        continue
    if(palavra_user == palavra_comp):
        print("Voce acertou!")
        print(f"numero de tentativas:{tentativas}")
        break
    else:
        for i in range(tamanho):
            a = 0
            b = 0
            usadas = []
            for j  in range(tamanho):
                if(i == j and palavra_user[i] == palavra_comp[i] and b==0 and palavra_user[i] not in usadas):
                    print(f"A letra \033[32m{palavra_user[i]}\033[m, posicao {i+1} esta correta.")
                    a = 1
                    usadas.append(palavra_user[i])
                    break
                if(palavra_user[i] == palavra_comp[j] and i!=j and a==0 and palavra_user[i] not in usadas):
                    print(f"A letra \033[33m{palavra_user[i]}\033[m esta correta mas na posicao errada.")
                    usadas.append(palavra_user[i])
                    b = 1
                    continue
            if(a==0 and b==0):
                print(f"A letra \033[31m{palavra_user[i]}\033[m esta errada")
                usadas.append(palavra_user[i])
        tentativas = tentativas + 1
        palavra_user = input("Tente de novo:")
        print(f"Tentativa {tentativas}/5")
if tentativas>5:
    print(f"Voce perdeu! A palavra correta era {palavra_comp}")
