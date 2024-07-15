class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome_completo = nome
        self.nascimento = data_nascimento
        self.documento = cpf
        self.localizacao = endereco
        self.contas_associadas = []

    def adicionar_conta(self, conta_bancaria):
        self.contas_associadas.append(conta_bancaria)

class RegistroHistorico:
    def __init__(self):
        self.transacoes_registradas = []

    def adicionar_registro(self, registro):
        self.transacoes_registradas.append(registro)

class ContaBancaria:
    def __init__(self, cliente, numero_conta, numero_agencia="0001"):
        self.saldo_atual = 0.0
        self.numero_conta = numero_conta
        self.numero_agencia = numero_agencia
        self.proprietario = cliente
        self.historico = RegistroHistorico()
        cliente.adicionar_conta(self)

    def efetuar_deposito(self, quantia):
        if quantia > 0:
            self.saldo_atual += quantia
            self.historico.adicionar_registro(f"Depósito: R$ {quantia:.2f}")
        else:
            print("Valor inválido para depósito.")

    def efetuar_saque(self, quantia):
        if quantia > self.saldo_atual:
            print("Saldo insuficiente.")
        elif quantia > 0:
            self.saldo_atual -= quantia
            self.historico.adicionar_registro(f"Saque: R$ {quantia:.2f}")
        else:
            print("Valor inválido para saque.")

    def mostrar_extrato(self):
        for registro in self.historico.transacoes_registradas:
            print(registro)
        print(f"\nSaldo: R$ {self.saldo_atual:.2f}")

class ContaCorrente(ContaBancaria):
    def __init__(self, cliente, numero_conta):
        super().__init__(cliente, numero_conta)
        self.limite_saque = 500.0
        self.limite_diario_saques = 3
        self.saques_realizados_hoje = 0

    def efetuar_saque(self, quantia):
        if self.saques_realizados_hoje >= self.limite_diario_saques:
            print("Limite diário de saques atingido.")
        elif quantia > self.limite_saque:
            print("Valor de saque excede o limite.")
        else:
            super().efetuar_saque(quantia)
            self.saques_realizados_hoje += 1

def criar_cliente(lista_clientes):
    nome = input("Digite o nome do cliente: ")
    nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    cpf = input("Digite o CPF do cliente: ")
    endereco = input("Digite o endereço do cliente (logradouro, número - bairro - cidade/estado): ")
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    if any(cliente.documento == cpf_numerico for cliente in lista_clientes):
        print("CPF já cadastrado!")
        return None
    return Cliente(nome, nascimento, cpf_numerico, endereco)

def criar_conta(lista_clientes, lista_contas):
    cpf = input("Digite o CPF do cliente para associar a conta: ")
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    cliente = next((cliente for cliente in lista_clientes if cliente.documento == cpf_numerico), None)
    if cliente:
        numero_conta = len(lista_contas) + 1
        nova_conta = ContaCorrente(cliente, numero_conta)
        lista_contas.append(nova_conta)
        print(f"Conta criada com sucesso para o cliente {cliente.nome_completo}!")
        return nova_conta
    else:
        print("Cliente não encontrado!")

def listar_clientes(lista_clientes):
    if not lista_clientes:
        print("Não há clientes cadastrados.")
    else:
        print("Lista de Clientes:")
        for idx, cliente in enumerate(lista_clientes, start=1):
            print(f"{idx}. Nome: {cliente.nome_completo} | CPF: {cliente.documento} | Endereço: {cliente.localizacao}")

def depositar(lista_contas):
    if not lista_contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para realizar o depósito: "))
    conta = next((conta for conta in lista_contas if conta.numero_conta == numero_conta), None)
    if conta:
        valor_deposito = float(input('Informe o valor de depósito: '))
        conta.efetuar_deposito(valor_deposito)
        print("Depósito realizado com sucesso!")
    else:
        print("Conta não encontrada.")

def sacar(lista_contas):
    if not lista_contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para realizar o saque: "))
    conta = next((conta for conta in lista_contas if conta.numero_conta == numero_conta), None)
    if conta:
        valor_saque = float(input("Informe o valor a ser sacado: "))
        conta.efetuar_saque(valor_saque)
    else:
        print("Conta não encontrada.")

def mostrar_extrato(lista_contas):
    if not lista_contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para exibir o extrato: "))
    conta = next((conta for conta in lista_contas if conta.numero_conta == numero_conta), None)
    if conta:
        conta.mostrar_extrato()
    else:
        print("Conta não encontrada.")

def menu_principal():
    clientes = []
    contas = []

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Criar cliente")
        print("2 - Criar conta")
        print("3 - Realizar depósito")
        print("4 - Realizar saque")
        print("5 - Exibir extrato")
        print("6 - Listar clientes")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            novo_cliente = criar_cliente(clientes)
            if novo_cliente:
                clientes.append(novo_cliente)
        elif escolha == "2":
            if clientes:
                criar_conta(clientes, contas)
            else:
                print("Não há clientes cadastrados!")
        elif escolha == "3":
            depositar(contas)
        elif escolha == "4":
            sacar(contas)
        elif escolha == "5":
            mostrar_extrato(contas)
        elif escolha == "6":
            listar_clientes(clientes)
        elif escolha == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
