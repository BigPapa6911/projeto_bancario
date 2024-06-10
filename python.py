import re
from datetime import datetime,timedelta
"""
=================================
 PRINTAR O MENU PARA SELEÇÃO
=================================
"""

menu = """
Menu
1 - Sacar
2 - Depositar
3 - Visualizar extrato
4 - Criar usuario
5 - Exibir usuario
6 - Criar conta corrente
7 - Sair
"""

menu = menu.strip()

largura = max(len(linha) for linha in menu.split("\n"))

menu_centralizado = '\n'.join(linha.center(30,' ') for linha in menu.split('\n'))

borda = "=" * (30)

menu_centralizado = f"{borda}\n {menu_centralizado}\n {borda}"

"""
=================================
DEFINIÇÃO DO SALDO
=================================
"""
saldo = 0
extrato = []
contador = 0
LIMITE_SAQUE = 3

saldo_formatado = "{:.2f}".format(saldo)

"""
=================================
 FUNÇÃO DE SAQUE
=================================
"""
def sacar():
    global saldo, extrato, contador, LIMITE_SAQUE
    if contador >= LIMITE_SAQUE:
        print("Limite diario de saque atingido")
    valor_de_saque = float(input("Qual valor você deseja sacar?"))
    if valor_de_saque > saldo : 
        print("Saldo insuficiente")
    if valor_de_saque > 500 :
        print("O valor limite para saque é de R$500,00")
    else:
        saldo -= valor_de_saque
        extrato.append(f"Saque: -R${valor_de_saque:.2f}")
        print(f"Saque de R${valor_de_saque:.2f} realizado")
        contador += 1
"""
=================================
 FUNÇÃO DE DEPOSITO
=================================
"""
def depositar():
    global saldo, extrato
    valor_de_deposito = float(input('Qual valor será depositado?'))
    saldo = saldo + valor_de_deposito
    extrato.append(f"Deposito: +R${valor_de_deposito:.2f}")
    print(f"Deposito de R${valor_de_deposito:.2f} realizado")
"""
=================================
 FUNÇÃO DE EXTRATO
=================================
"""
def exibir_extrato():
    global saldo, extrato
    print("Extrato:")
    if not extrato:
        print("Nenhuma transação ocorrida")
    else:
        for transacoes in extrato :
            print(transacoes)
        print(f"Saldo atual: R${saldo:.2f}")
"""
=================================
 FUNÇÃO DE CRIAR USUARIO
=================================
"""
usuarios = {}

estados_brasil = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO"
}

"""
=================================
 VALIDAR CPF
=================================
"""
def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Verificação do dígito verificador
    def calcular_digito(cpf, fator):
        soma = 0
        for i in range(fator - 1):
            soma += int(cpf[i]) * (fator - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf, 10)
    digito2 = calcular_digito(cpf, 11)

    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

"""
=================================
VALIDAR DATA
=================================
"""

def validar_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def validar_data_nascimento(data_nascimento):
    if not validar_data(data_nascimento):
        return False
    data_nascimento_dt = datetime.strptime(data_nascimento, '%d/%m/%Y')
    idade = (datetime.now() - data_nascimento_dt).days / 365.25
    return idade >= 18


def criar_usuario():
    nome = input("Digite seu nome:")
    data_nascimento = input("Qual sua data de nascimento (DD/MM/AAAA)? ")
    if not validar_data_nascimento(data_nascimento):
        print("Data de nascimento inválida ou menor de idade.")
        return

    cpf = input("Qual seu CPF? ")
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return
    
    logradouro=input("Qual logradouro de sua casa?")
    numero=input("Qual o numero da sua casa?")
    bairro=input("Qual seu bairro?")
    cidade=input("Qual sua cidade?")

    cpf = cpf.replace(".","").replace("-","")

    estados_lista = list(estados_brasil.keys())

    for indice, estados in enumerate(estados_lista, start=1):
        print(f"{indice}- {estados_brasil[estados]}")
    estado_numero = int(input("Selecione seu estado:"))

    if estado_numero<1 or estado_numero>len(estados_lista):
        print("Valor invalido")
        return
    
    estado_selecionado = estados_lista[estado_numero - 1]
    estado_sigla = estados_brasil[estado_selecionado]

    if cpf in usuarios:
        print("CPF já cadastrado")
        return
    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado_sigla}"

    usuarios[cpf] = {
        "nome" : nome,
        "data_nascimento" : data_nascimento,
        "endereco" : endereco,
        "contas_correntes": []
    }

    print("Usario criado")
"""
=================================
 FUNÇÃO DE PRINTAR USUARIO
=================================
"""
def printar_usuario():
     for cpf, dados in usuarios.items():
        nome = dados["nome"]
        data_nascimento = dados["data_nascimento"]
        endereco = dados["endereco"]
        contas_correntes = dados["contas_correntes"]
        
        print(f"Nome: {nome}, CPF: {cpf}, Data de Nascimento: {data_nascimento}")
        print(f"Endereço: {endereco}\n")
        if contas_correntes:
            for conta in contas_correntes:
                print(f"Conta Corrente - Agencia: {conta['agencia']}, Conta: {conta['numero_conta']}")
        else:
            print("Conta Corrente: Não possui")
        print("\n")

"""
=================================
CRIAR CONTA CORRENTE
=================================
"""
agencia = "0001"
numero_conta = 1


def criar_conta_corrente():

    global numero_conta

    cpf_lista = list(usuarios.keys())

    for indice, usuario in enumerate(usuarios,start=1):
        print(f"{indice} - {usuario}")

    usuario_conta = input("Você deseja criar uma conta para qual CPF?").replace('.', '').replace('-', '')

    if usuario_conta in usuarios:
        usuario_conta = usuario_conta
    elif usuario_conta.isdigit():
        indice = int(usuario_conta)
        if 1 <= indice <= len(cpf_lista):
            usuario_conta = cpf_lista[indice - 1]
        else:
            print("Índice inválido.")
            return
    elif usuario_conta not in usuarios:
        print("CPF não encontrado!!")
        return

    nova_conta = {
        "agencia": agencia,
        "numero_conta": f"{numero_conta:06d}"
    }

    if "contas_correntes" not in usuarios[usuario_conta]:
        usuarios[usuario_conta]["contas_correntes"] = []

    usuarios[usuario_conta]["contas_correntes"].append(nova_conta)


    print(f"""Conta criada com sucesso!!
          CPF  - {usuario_conta}
          Agencia : {nova_conta['agencia']} 
          Conta: {nova_conta['numero_conta']}""")

    numero_conta += 1 


"""
=================================
 SELECIONAR FUNÇÃO
=================================
"""

while True :

    print(menu_centralizado)

    operação = int(input("Selecione a operação:"))

    if operação == 1 :
        sacar()
    elif operação == 2  :
        depositar()
    elif operação == 3 :
        exibir_extrato()
    elif operação == 4 :
        criar_usuario()
    elif operação == 5 :
        printar_usuario()
    elif operação == 6 :
        criar_conta_corrente()
    elif operação == 7 :
        print("Saindo")
        break
    else:
        print("Operação invalida")
