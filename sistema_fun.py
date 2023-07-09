import os
import time
from time import sleep
menu = """
seja bem vindo ao sistema bancário.
selecione o tipo de acesso:
[a] Admin
[c] Cliente
[q] Sair
=> """
menu_administrador = """
[c] Criar usuário
[a] Criar conta
[l] listar usuários
[t] listar contas
[q] Sair
=> """

menu_usuario = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """
USUARIO = "admin"
SENHA = "admin"
LIMITE_SAQUES = 3

limite = 500
numero_saques = 0


usuarios = {}
usuarios["38318235029"] = {"nome": "João", "cpf": "38318235029","data_nascimento": "01-01-2000", "endereco": "Rua 1, 123 - Centro - São Paulo/SP"}
usuarios["33136917065"] = {"nome": "Maria", "cpf": "33136917065","data_nascimento": "01-01-2000", "endereco": "Rua 1, 123 - Centro - São Paulo/SP"}

contas = {}
contas["38318235029"] = {"agencia": "0001", "numero_conta": "1234-5","usuario": "38318235029","saldo": 0.0,"extrato" : ""}
contas["33136917065"] = {"agencia": "0001", "numero_conta": "1235-6","usuario": "33136917065","saldo": 0.0,"extrato" : ""}


def criar_usuario():
    cpf = input("Digite o CPF (apenas números): ")

    if cpf in usuarios:
        print("Usuário já cadastrado")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios[cpf] = {"nome": nome, "cpf": cpf,"data_nascimento": data_nascimento, "endereco": endereco}
    print("Usuário cadastrado com sucesso.")
    sleep(1)
def criar_conta():
    cpf = input("Digite o CPF do titular da conta (apenas números): ")
    
    if cpf in usuarios:
        agencia = input("Digite a agência: ")
        numero_conta = input("Digite o número da conta: ")
        contas[cpf] = {"agencia": agencia, "numero_conta": numero_conta, "usuario": cpf, "saldo": 0.0, "extrato": ""}
        print("Conta criada com sucesso.")
        sleep(1)
    print("Usuário não encontrado.")
def deposito(valor,cpf,/):
    extrato = ""
    if valor <= 0:
        print("Operação inválida")
    else:
        contas[cpf]["saldo"] += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        contas[cpf]["extrato"] += extrato
        print("Depósito realizado com sucesso!")
        sleep(1)
def saque(*,valor,cpf,numero_saques):
    if valor > contas[cpf]["saldo"]:
        limpar_escrever("Não é possível sacar o dinheiro pois não tem saldo suficiente")
    elif valor > limite:
        limpar_escrever("Você excedeu o limite de valor de transação")
    elif numero_saques >= LIMITE_SAQUES:
        limpar_escrever("Você excedeu o número de saques")
    elif valor > 0:
        
        contas[cpf]["saldo"] -= valor
        contas[cpf]["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        limpar_escrever("Saque realizado com sucesso!")
    else:
        print("Operação inválida")
        sleep(1)
    return numero_saques+1
def mostrar_extrato(cpf):
    print("\nEXTRATO\n")
    if contas[cpf]["extrato"] == "":
        print("Não foram efetuadas movimentações.")
        regressiva()
    else:
        print(contas[cpf]["extrato"] )
        saldo = contas[cpf]["saldo"] 
        print(f"Saldo:\t\tR$ {saldo:.2f}\n")
        regressiva()
def limpar_escrever(texto, dado="padrao"):
    if dado != "padrao":
        os.system('cls')
        dado = input(f'{texto}')
        return dado
    else:
        os.system('cls')
        print(f'{texto}')
        sleep(1)
def regressiva():
    print("limpando listagem em:")
    for i in range(10, -1, -1):
        print(f"\b\b\b{i} ", end="", flush=True)
        time.sleep(0.5)


while True:
    opcao = limpar_escrever(menu, "menu")
    if opcao == "a":
        usuario = input("digite o usuário:")
        senha = input("digite a senha:")
        if usuario == USUARIO and senha == SENHA:
            limpar_escrever('Login Efetuado com sucesso.')
            while True:
                opcao = limpar_escrever(menu_administrador, "admin")
                if opcao == "c":
                    limpar_escrever("Cadastrar usuário")
                    criar_usuario()
                elif opcao == "a":
                    limpar_escrever("criação de contas")                    
                    criar_conta()
                elif opcao == "l":
                    print("Listagem de usuários")
                    for usuario in usuarios:
                        print(f"{usuarios[usuario]['nome']} - {usuario}")
                    regressiva()
                elif opcao == "t":
                    print("Listagem de contas")
                    # print(f"{contas}")
                    for conta in contas:
                        agencia = contas[conta]["agencia"]
                        numero_conta = contas[conta]["numero_conta"]
                        cpf_usuario = contas[conta]["usuario"]
                        nome_usuario = usuarios[cpf_usuario]["nome"]
                        print(f"agencia: {agencia} conta:{numero_conta} - {nome_usuario}")
                    regressiva()
                elif opcao == "q":
                    break
                else:
                    limpar_escrever("Operação inválida, por favor, selecione a operação desejada.")

        else:
            limpar_escrever('dados inválidos')
    elif opcao == "c":
        cpf = input('digite o seu CPF (somente números)')
        while True:
            if cpf in usuarios:
                opcao = limpar_escrever(menu_usuario, "usuario")
                if opcao == "d":
                    valor = float(input("Digite o valor do depósito: "))
                    deposito(valor,cpf)
                elif opcao == "s":
                    if numero_saques >= LIMITE_SAQUES:
                        limpar_escrever("Você excedeu o número de saques")
                    else:
                        valor = float(input("Digite o valor do saque: "))
                        numero_saques = saque(valor=valor,cpf=cpf,numero_saques=numero_saques)
                elif opcao == "e":
                    mostrar_extrato(cpf)
                elif opcao == "q":
                    break
                else:
                    limpar_escrever("Operação inválida, por favor, selecione a operação desejada.")
            else:
                limpar_escrever('Usuário não cadastrado \n')
                break

    elif opcao == "q":
        break
    else:
        limpar_escrever(
            "Operação inválida, por favor, selecione a operação desejada.")
