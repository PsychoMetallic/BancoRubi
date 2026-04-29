# BancoRubi
import json
import hashlib
import os
import random
import string
from datetime import datetime
import time

def anim(texto):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(0.05)
    print()

ARQUIVO = "banco.json"
MAX_TENTATIVAS = 3

# Criar arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump({}, f)

def gerar_salt():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def criptografar(senha, salt):
    return hashlib.sha256((senha + salt).encode()).hexdigest()

def carregar():
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

# =========================
# CRIAR CONTA
# =========================
def criar_conta():
    dados = carregar()
    
    usuario = input("Crie um usuário: ")
    
    if usuario in dados:
        print("Usuário já existe!")
        return
    
    while True:
        senha = input("Crie uma senha (EXATAMENTE 8 números): ")
        
        if len(senha) != 8 or not senha.isdigit():
            print("A senha deve ter exatamente 8 dígitos numéricos!")
        else:
            break
    
    salt = gerar_salt()
    senha_hash = criptografar(senha, salt)
    
    dados[usuario] = {
        "senha": senha_hash,
        "salt": salt,
        "saldo": 0,
        "historico": []
    }
    
    salvar(dados)
    print("Conta criada com sucesso!")

# =========================
# LOGIN
# =========================
def login():
    dados = carregar()
    
    usuario = input("Usuário: ")
    
    if usuario not in dados:
        anim("Usuário não existe!")
        return
    
    tentativas = 0
    
    while tentativas < MAX_TENTATIVAS:
        senha = input("Senha: ")
        
        salt = dados[usuario]["salt"]
        senha_hash = criptografar(senha, salt)
        
        if senha_hash == dados[usuario]["senha"]:
            anim("Login realizado!")
            menu_usuario(usuario)
            return
        else:
            tentativas += 1
            anim(f"Senha incorreta! Restam {MAX_TENTATIVAS - tentativas}")
    
    anim("Conta bloqueada!")

# =========================
# MENU DO USUÁRIO
# =========================
def menu_usuario(usuario):
    while True:
        print(f"\n=== Bem-vindo, ao Banco-Rubi {usuario} ===")
        anim("1 - Ver saldo")
        anim("2 - Depositar")
        anim("3 - Transferir")
        anim("4 - Histórico")
        anim("5 - Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            ver_saldo(usuario)
        elif opcao == "2":
            depositar(usuario)
        elif opcao == "3":
            transferir(usuario)
        elif opcao == "4":
            ver_historico(usuario)
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")

# =========================
# FUNÇÕES BANCÁRIAS
# =========================
def ver_saldo(usuario):
    dados = carregar()
    anim(f"Saldo: R${dados[usuario]['saldo']}")

def depositar(usuario):
    dados = carregar()
    
    valor = float(input("Valor para depositar: "))
    
    dados[usuario]["saldo"] += valor
    
    dados[usuario]["historico"].append(
        f"{datetime.now()} - Depósito de R${valor}"
    )
    
    salvar(dados)
    anim("Depósito realizado!")

def transferir(usuario):
    dados = carregar()
    
    destino = input("Usuário destino: ")
    
    if destino not in dados:
        anim("Usuário não encontrado!")
        return
    
    valor = float(input("Valor da transferência: "))
    
    if dados[usuario]["saldo"] < valor:
        anim("Saldo insuficiente!")
        return
    
    dados[usuario]["saldo"] -= valor
    dados[destino]["saldo"] += valor
    
    data = datetime.now()
    
    dados[usuario]["historico"].append(
        f"{data} - Transferiu R${valor} para {destino}"
    )
    
    dados[destino]["historico"].append(
        f"{data} - Recebeu R${valor} de {usuario}"
    )
    
    salvar(dados)
    anim("Transferência realizada!")

def ver_historico(usuario):
    dados = carregar()
    
    print("\n=== HISTÓRICO ===")
    for item in dados[usuario]["historico"]:
        anim(item)

# =========================
# MENU PRINCIPAL
# =========================
while True:
    anim("\n=== BANCO-RUBI ===")
    anim("1 - Criar conta")
    anim("2 - Login")
    anim("3 - Sair")
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        criar_conta()
    elif opcao == "2":
        login()
    elif opcao == "3":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")