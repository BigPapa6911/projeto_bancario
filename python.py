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
4 - Sair
"""

menu = menu.strip()

largura = max(len(linha) for linha in menu.split("\n"))

menu_centralizado = '\n'.join(linha.center(30,' ') for linha in menu.split('\n'))

borda = "=" * (30)

menu_centralizado = f"{borda}\n {menu_centralizado}\n {borda}"

print(menu_centralizado)

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
 SELECIONAR FUNÇÃO
=================================
"""

while True :
    operação = int(input("Selecione a operação:"))

    if operação == 1 :
        if contador >= LIMITE_SAQUE:
            print("Limite diario de saque atingido")
            continue
        sacar = float(input("Qual valor você deseja sacar?"))
        if sacar > saldo : 
            print("Saldo insuficiente")
        if sacar > 500 :
            print("O valor limite para saque é de R$500,00")
        else:
            saldo -= sacar
            extrato.append(f"Saque: -R${sacar:.2f}")
            contador += 1
    elif operação == 2  :
        depositar = float(input('Qual valor será depositado?'))
        saldo = saldo + depositar
        extrato.append(f"Deposito: +R${depositar:.2f}")
    elif operação == 3 :
        print("Extrato:")
        if not extrato:
            print("Nenhuma transação ocorrida")
        else:
            for transacoes in extrato :
                print(transacoes)
            print(f"Saldo atual: R${saldo:.2f}")
    elif operação ==4 :
        print("Saindo")
        break
    else:
        print("Operação invalida")
