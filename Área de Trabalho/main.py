import json

# Classe para representar um usuário
class Usuario:
    def __init__(self, nome, cpf_cnpj, endereco, telefone, senha):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.endereco = endereco
        self.telefone = telefone
        self.senha = senha
        self.conta = Conta()

# Classe para representar a conta do usuário
class Conta:
    def __init__(self):
        self.saldo = 0
        self.historico = []

    def depositar(self, valor):
        self.saldo += valor
        self.historico.append(f'Depósito: R${valor:.2f}')

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            self.historico.append(f'Saque: R${valor:.2f}')
        else:
            print("Saldo insuficiente.")

    def adicionar_historico(self, operacao):
        self.historico.append(operacao)

    def obter_saldo(self):
        return self.saldo

# Classe para representar o caixa eletrônico
class CaixaEletronico:
    def __init__(self):
        self.usuarios = {}
        self.usuario_mestre = None

    def cadastrar_usuario(self, nome, cpf_cnpj, endereco, telefone, senha):
        usuario = Usuario(nome, cpf_cnpj, endereco, telefone, senha)
        self.usuarios[cpf_cnpj] = usuario

    def remover_usuario(self, cpf_cnpj, senha_mestre):
        if self.usuario_mestre is not None and self.usuario_mestre.senha == senha_mestre:
            if cpf_cnpj in self.usuarios:
                usuario = self.usuarios[cpf_cnpj]
                usuario.conta.saldo = 0
                del self.usuarios[cpf_cnpj]
                print("Usuário removido com sucesso.")
            else:
                print("Usuário não encontrado.")
        else:
            print("Senha mestre incorreta.")

    def realizar_login(self, cpf_cnpj, senha):
        if cpf_cnpj in self.usuarios:
            usuario = self.usuarios[cpf_cnpj]
            if usuario.senha == senha:
                return usuario
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")

    def exibir_historico(self, cpf_cnpj):
        if cpf_cnpj in self.usuarios:
            usuario = self.usuarios[cpf_cnpj]
            for operacao in usuario.conta.historico:
                print(operacao)
        else:
            print("Usuário não encontrado.")

    #Recebe as informações do cliente, salva em uma matriz e envia essas informações para um arquivo
    def salvar_dados(self):
        dados = {
            "usuarios": {}
        }

        for cpf_cnpj, usuario in self.usuarios.items():
            dados["usuarios"][cpf_cnpj] = {
                "nome": usuario.nome,
                "endereco": usuario.endereco,
                "telefone": usuario.telefone,
                "senha": usuario.senha,
                "conta": {
                    "saldo": usuario.conta.saldo,
                    "historico": usuario.conta.historico
                }
            }

        with open("dados.json", "w") as arquivo:
            json.dump(dados, arquivo)

    def carregar_dados(self):
        try:
            with open("dados.json", "r") as arquivo:
                dados = json.load(arquivo)
                for cpf_cnpj, info_usuario in dados["usuarios"].items():
                    usuario = Usuario(info_usuario["nome"], cpf_cnpj, info_usuario["endereco"],
                                      info_usuario["telefone"], info_usuario["senha"])
                    usuario.conta.saldo = info_usuario["conta"]["saldo"]
                    usuario.conta.historico = info_usuario["conta"]["historico"]
                    self.usuarios[cpf_cnpj] = usuario

            print("Dados carregados com sucesso.")
        except FileNotFoundError:
            print("Arquivo de dados não encontrado.")

# Função para exibir o menu principal
def exibir_menu():
    print("1. Cadastrar usuário")
    print("2. Remover usuário (usuário mestre)")
    print("3. Realizar login")
    print("4. Exibir histórico")
    print("5. Sair")

# Função para ler uma opção do menu
def ler_opcao():
    while True:
        try:
            opcao = int(input("Digite uma opção: "))
            return opcao
        except ValueError:
            print("Opção inválida. Digite um número.")

# Função para ler os dados de um novo usuário
def ler_dados_usuario():
    nome = input("Digite o nome: ")
    cpf_cnpj = input("Digite o CPF ou CNPJ: ")
    endereco = input("Digite o endereço: ")
    telefone = input("Digite o telefone (no formato 61-99698-6360): ")
    senha = input("Digite a senha (6 dígitos numéricos): ")
    return nome, cpf_cnpj, endereco, telefone, senha

# Função para ler os dados do usuário mestre
def ler_dados_usuario_mestre():
    cpf_cnpj = input("Digite o CPF ou CNPJ do usuário mestre: ")
    senha = input("Digite a senha do usuário mestre: ")
    return cpf_cnpj, senha

# Função para ler os dados de login
def ler_dados_login():
    cpf_cnpj = input("Digite o CPF ou CNPJ: ")
    senha = input("Digite a senha: ")
    return cpf_cnpj, senha

# Função para ler os dados de uma transação
def ler_dados_transacao():
    valor = float(input("Digite o valor da transação: "))
    return valor

# Função para exibir o menu de transações
def exibir_menu_transacoes():
    print("1. Saque")
    print("2. Depósito")
    print("3. Realizar pagamento programado")
    print("4. Solicitar crédito")
    print("5. Voltar")

# Função principal
def main():
    caixa = CaixaEletronico()
    caixa.carregar_dados()

    while True:
        exibir_menu()
        opcao = ler_opcao()

        if opcao == 1:
            nome, cpf_cnpj, endereco, telefone, senha = ler_dados_usuario()
            caixa.cadastrar_usuario(nome, cpf_cnpj, endereco, telefone, senha)
            caixa.salvar_dados()
            print("Usuário cadastrado com sucesso.")

        elif opcao == 2:
            cpf_cnpj, senha_mestre = ler_dados_usuario_mestre()
            caixa.remover_usuario(cpf_cnpj, senha_mestre)
            caixa.salvar_dados()

        elif opcao == 3:
            cpf_cnpj, senha = ler_dados_login()
            usuario = caixa.realizar_login(cpf_cnpj, senha)

            if usuario is not None:
                while True:
                    exibir_menu_transacoes()
                    opcao_transacao = ler_opcao()

                    if opcao_transacao == 1:
                        valor = ler_dados_transacao()
                        usuario.conta.sacar(valor)
                        usuario.conta.adicionar_historico(f"Saque: R${valor:.2f}")
                        caixa.salvar_dados()

                    elif opcao_transacao == 2:
                        valor = ler_dados_transacao()
                        usuario.conta.depositar(valor)
                        usuario.conta.adicionar_historico(f"Depósito: R${valor:.2f}")
                        caixa.salvar_dados()

                    elif opcao_transacao == 3:
                        print("Funcionalidade em desenvolvimento.")

                    elif opcao_transacao == 4:
                        print("Funcionalidade em desenvolvimento.")

                    elif opcao_transacao == 5:
                        break

                    else:
                        print("Opção inválida.")

        elif opcao == 4:
            cpf_cnpj, _ = ler_dados_login()
            caixa.exibir_historico(cpf_cnpj)

        elif opcao == 5:
            caixa.salvar_dados()
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()