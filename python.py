from abc import ABC, abstractmethod, abstractproperty
import re
import textwrap
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar_transacao(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return float(self._saldo)

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("Saldo insuficiente")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado")
            return True
        else:
            print("Operação falhou!!")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Deposito de R${valor:.2f} realizado")
        else:
            print("Valor invalido!!")
            return False
        return True

class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_feitos = 0

    def sacar(self, valor):
        if valor > self.limite:
            print("Valor acima do limite estabelecido!!")
        elif self.saques_feitos >= self.limite_saques:
            print("Limite diário de saques atingido!!")
        else:
            if super().sacar(valor):
                self.saques_feitos += 1
                return True
        return False

    def __str__(self) -> str:
        return f"""
                Nome: {self.cliente.nome}
                Conta Corrente - Agencia: {self.agencia}, Conta: {self.numero}
        """

class Historico:
    def __init__(self):
        self._extrato = []

    @property
    def extrato(self):
        return self._extrato

    def adicionar_transacao(self, transacao):
        self._extrato.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar_transacao(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar_transacao(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar_transacao(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def print_menu():
    menu = """
    Menu
    1 - Sacar
    2 - Depositar
    3 - Visualizar extrato
    4 - Criar usuario
    5 - Exibir contas
    6 - Criar conta corrente
    7 - Sair
    """
    menu = menu.strip()
    menu_centralizado = '\n'.join(linha.center(30, ' ') for linha in menu.split('\n'))
    borda = "=" * 30
    menu_centralizado = f"{borda}\n{menu_centralizado}\n{borda}"
    print(menu_centralizado)

def achar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente sem conta!!")
        return
    for i, conta in enumerate(cliente.contas):
        print(f"{i + 1} - Agencia: {conta.agencia}, Conta: {conta.numero}")
    escolha = int(input("Escolha o número da conta: ")) - 1
    if escolha < 0 or escolha >= len(cliente.contas):
        print("Conta inválida!")
        return
    return cliente.contas[escolha]

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    def calcular_digito(cpf, fator):
        soma = 0
        for i in range(fator - 1):
            soma += int(cpf[i]) * (fator - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf, 10)
    digito2 = calcular_digito(cpf, 11)

    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def validar_data(data):
    try:
        datetime.strptime(data, '%d%m%Y')
        return True
    except ValueError:
        return False

def validar_data_nascimento(data_nascimento):
    if not validar_data(data_nascimento):
        return False
    data_nascimento_dt = datetime.strptime(data_nascimento, '%d%m%Y')
    idade = (datetime.now() - data_nascimento_dt).days / 365.25
    return idade >= 18

def sacar(clientes):
    cpf = input("Informe o CPF do cliente:").replace('.', '').replace('-', '')
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!!")
        return

    conta = achar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Qual será o valor sacado?"))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente:").replace('.', '').replace('-', '')
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!!")
        return

    conta = achar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Qual será o valor depositado?"))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:").replace('.', '').replace('-', '')
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!!")
        return

    conta = achar_conta_cliente(cliente)
    if not conta:
        return

    print("Extrato:")
    transacoes = conta.historico.extrato
    extrato = ""

    if not transacoes:
        print("Nenhuma transação ocorrida")
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']} : \t R${transacao['valor']:.2f}"
    print(extrato)
    print(f"Saldo atual: R${conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input("Informe o CPF:").replace('.', '').replace('-', '')
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("CPF já utilizado!!")
        return

    nome = input("Digite seu nome:")
    data_nascimento = input("Qual sua data de nascimento (DD/MM/AAAA)? ").replace('/', '').replace('-', '')
    if not validar_data_nascimento(data_nascimento):
        print("Data de nascimento inválida ou menor de idade.")
        return

    logradouro = input("Qual logradouro de sua casa?")
    numero = input("Qual o número da sua casa?")
    bairro = input("Qual seu bairro?")
    cidade = input("Qual sua cidade?")

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
    estados_lista = list(estados_brasil.keys())

    for indice, estados in enumerate(estados_lista, start=1):
        print(f"{indice} - {estados_brasil[estados]}")
    estado_numero = int(input("Selecione seu estado:"))

    if estado_numero < 1 or estado_numero > len(estados_lista):
        print("Valor invalido")
        return

    estado_selecionado = estados_lista[estado_numero - 1]
    estado_sigla = estados_brasil[estado_selecionado]

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado_sigla}"

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("Cliente criado com Sucesso")

def printar_contas(contas):
    if not contas:
        print("Nenhuma conta encontrada!!")
        return
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_conta(numero_conta, clientes, contas):
    for indice, usuario in enumerate(clientes, start=1):
        print(f"{indice} - {usuario.nome} - {usuario.cpf}")

    cpf = input("Você deseja criar uma conta para qual CPF?").replace('.', '').replace('-', '')
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!!")
        return

    conta = Conta_corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!!")

def main():
    clientes = []
    contas = []

    while True:
        print_menu()
        operacao = int(input("Selecione a operação:"))

        if operacao == 1:
            sacar(clientes)
        elif operacao == 2:
            depositar(clientes)
        elif operacao == 3:
            exibir_extrato(clientes)
        elif operacao == 4:
            criar_cliente(clientes)
        elif operacao == 5:
            printar_contas(contas)
        elif operacao == 6:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif operacao == 7:
            print("Saindo")
            break
        else:
            print("Operação invalida")

main()
