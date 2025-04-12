import os
import re
from datetime import datetime


COR_MAGENTA = "\033[35m"
COR_AMARELO = "\033[33m"
COR_CYAN = "\033[96m"
COR_VERDE = "\033[92m"
COR_VERMELHO = "\033[91m"

def carregar_carros():
    carros = {}
    if os.path.exists("carros.txt.txt"):
        with open("carros.txt.txt", "r") as file:
            for linha in file:
                if linha.strip():
                    dados = linha.strip().split(',')
                    if len(dados) == 4:
                        try:
                            id_carro = int(dados[0])
                            modelo = dados[1]
                            disponivel = dados[2].strip().lower() == "sim"
                            preco = float(dados[3])
                            carros[id_carro] = {'modelo': modelo, 'disponivel': disponivel, 'preco': preco}
                        except ValueError:
                            print(f"{COR_VERMELHO}Erro ao processar o carro: {linha}. ID deve ser um número.")
    return carros

def adicionar_carro(carros):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            id_carro = int(input(f"{COR_CYAN}Digite o ID do novo carro: "))
            if id_carro in carros:
                print(f"{COR_VERMELHO}Já existe um carro com esse ID.")
                opcao = input(f"{COR_AMARELO}Deseja tentar novamente? (S para sim, pressione enter para voltar ao menu): ").strip().lower()
                if opcao != 's':
                    break
            else:
                modelo = input(f"{COR_CYAN}Digite o modelo do novo carro: ").strip()
                disponivel = input(f"{COR_CYAN}Está disponível? (sim/não): ").strip().lower()
                if disponivel not in ["sim", "não"]:
                    print(f"{COR_VERMELHO}Opção inválida para disponibilidade. Por favor, insira 'sim' ou 'não'.")
                    continue
                
                try:
                    preco = float(input(f"{COR_CYAN}Digite o preço por dia do carro: R$ ").strip())
                except ValueError:
                    print(f"{COR_VERMELHO}Por favor, insira um valor válido para o preço.")
                    continue

                carros[id_carro] = {'modelo': modelo, 'disponivel': disponivel == "sim", 'preco': preco}
                print(f"{COR_VERDE}Carro {modelo} adicionado com sucesso!")
                salvar_carros(carros)
                input(f"{COR_CYAN}\nPressione enter para voltar ao menu. ")  
                break
        except ValueError:
            print(f"{COR_VERMELHO}Por favor, insira um número válido para o ID.")
            opcao = input(f"{COR_AMARELO}Deseja tentar novamente? (S para sim, pressione enter para voltar ao menu): ").strip().lower()
            if opcao != 's':
                break
            
            
def remover_carro(carros):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COR_MAGENTA}\nRemover um carro:")

        carros_disponiveis = [id_carro for id_carro, info in carros.items() if info['disponivel']]
        
        if carros_disponiveis:
            print(f"{COR_CYAN}Carros disponíveis para remoção:")
            for id_carro in carros_disponiveis:
                modelo = carros[id_carro]['modelo']
                print(f"{COR_AMARELO}ID: {id_carro} | Modelo: {modelo}")

            try:
                id_carro = int(input(f"{COR_CYAN}Digite o ID do carro que deseja remover: "))
                if id_carro in carros_disponiveis:
                    modelo = carros[id_carro]['modelo']
                    confirmar = input(f"{COR_AMARELO}Tem certeza que deseja remover o carro {modelo}? (S para sim, pressione enter para cancelar): ").strip().lower()
                    if confirmar == 's':
                        del carros[id_carro]
                        print(f"{COR_VERDE}Carro {modelo} removido com sucesso!")
                        salvar_carros(carros)
                        input(f"{COR_CYAN}\nPressione enter para voltar ao menu. ")  
                        break
                    else:
                        print(f"{COR_VERMELHO}Operação de remoção cancelada.")
                else:
                    print(f"{COR_VERMELHO}Carro não encontrado ou ID inválido.")
            except ValueError:
                print(f"{COR_VERMELHO}Por favor, insira um número válido para o ID.")
        else:
            print(f"{COR_VERMELHO}Não há carros disponíveis para remoção no momento.")
        
        opcao = input(f"{COR_AMARELO}Deseja tentar novamente? (S para sim, pressione enter para voltar ao menu): ").strip().lower()
        if opcao != 's':
            break

def salvar_carros(carros):
    with open("carros.txt.txt", "w") as file:
        for id_carro, info in carros.items():
            disponivel = "sim" if info['disponivel'] else "não"
            file.write(f"{id_carro},{info['modelo']},{disponivel},{info['preco']}\n")

def carregar_clientes():
    clientes = {}
    if os.path.exists("clientes.txt"):
        with open("clientes.txt", "r") as file:
            for linha in file:
                if linha.strip():
                    dados = linha.strip().split(',')
                    if len(dados) == 6:
                        nome, cnh, email, telefone, data_nascimento, endereco = dados
                        clientes[cnh] = {'nome': nome, 'email': email, 'telefone': telefone, 'data_nascimento': data_nascimento, 'endereco': endereco}
    return clientes

def salvar_clientes(clientes):
    with open("clientes.txt", "w") as file:
        for cnh, info in clientes.items():
            file.write(f"{info['nome']},{cnh},{info['email']},{info['telefone']},{info['data_nascimento']},{info['endereco']}\n")

def listar_carros_disponiveis(carros):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nCarros disponíveis para aluguel:")
    carros_disponiveis = False
    for id_carro, info in carros.items():
        if info['disponivel']:
            print(f"{COR_AMARELO}ID: {id_carro} | Modelo: {info['modelo']} | Preço por dia: R$ {info['preco']:.2f} | Disponível: {'Sim' if info['disponivel'] else 'Não'}")
            carros_disponiveis = True
    if not carros_disponiveis:
        print(f"{COR_VERMELHO}Nenhum carro disponível no momento.")
    input(f"{COR_CYAN}\nPressione Enter para voltar ao menu.")

def listar_carros_alugados(carros):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nCarros alugados:")
    carros_alugados = False
    for id_carro, info in carros.items():
        if not info['disponivel']:
            print(f"{COR_AMARELO}ID: {id_carro} | Modelo: {info['modelo']} | Disponível: {'Sim' if info['disponivel'] else 'Não'}")
            carros_alugados = True
    if not carros_alugados:
        print(f"{COR_VERMELHO}Nenhum carro alugado no momento.")
    input(f"{COR_CYAN}\nPressione Enter para voltar ao menu.")

def buscar_carro(carros):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nBuscar por carro:")
    try:
        id_carro = int(input(f"{COR_CYAN}Digite o ID do carro: "))
        if id_carro in carros:
            info = carros[id_carro]
            print(f"{COR_AMARELO}ID: {id_carro} | Modelo: {info['modelo']} | Preço por dia: R$ {info['preco']:.2f} | Disponível: {'Sim' if info['disponivel'] else 'Não'}")
        else:
            print(f"{COR_VERMELHO}Carro não encontrado.")
    except ValueError:
        print(f"{COR_VERMELHO}Por favor, insira um número válido para o ID.")
    input(f"{COR_CYAN}\nPressione enter para voltar ao menu.")


def alugar_carro(carros, clientes):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nAlugar um carro:")

    nome_cliente = input(f"{COR_CYAN}Digite seu nome completo: ").strip()
    cnh_cliente = input(f"{COR_CYAN}Digite seu número de CNH: ").strip()

    if cnh_cliente not in clientes:
        input(f"{COR_VERMELHO}Você não está cadastrado. Por favor, faça seu cadastro antes de alugar um carro. Pressione enter para retornar ao menu.")
        return

    carros_disponiveis = [id_carro for id_carro, info in carros.items() if info['disponivel']]
    
    if carros_disponiveis:
        print(f"{COR_CYAN}Carros disponíveis para aluguel:")
        for id_carro in carros_disponiveis:
            modelo = carros[id_carro]['modelo']
            preco = carros[id_carro]['preco']
            print(f"{COR_AMARELO}ID: {id_carro} | Modelo: {modelo} | Preço por dia: R$ {preco:.2f}")

        try:
            id_carro = int(input(f"{COR_CYAN}Digite o ID do carro que deseja alugar: "))
            if id_carro in carros_disponiveis:
                info = carros[id_carro]
                dias = int(input(f"{COR_CYAN}Quantos dias você deseja alugar o carro {info['modelo']}? "))
                if dias > 0:
                    custo_total = dias * info['preco']
                    print(f"{COR_VERDE}O custo total pelo aluguel de {dias} dias é: R$ {custo_total:.2f}")
                    confirmar = input(f"{COR_AMARELO}Deseja confirmar o aluguel? (S para sim, pressione enter para cancelar): ").strip().lower()
                    if confirmar == 's':
                        info['disponivel'] = False

                        clientes[cnh_cliente]['carro_alugado'] = {'id': id_carro, 'modelo': info['modelo'], 'dias': dias, 'custo': custo_total}
                        print(f"{COR_VERDE}Carro {info['modelo']} alugado com sucesso! Custo total: R$ {custo_total:.2f}")
                        salvar_carros(carros)
                        salvar_clientes(clientes)
                    else:
                        print(f"{COR_VERMELHO}Aluguel cancelado.")
                else:
                    print(f"{COR_VERMELHO}Número de dias inválido.")
            else:
                print(f"{COR_VERMELHO}Carro não disponível ou ID inválido.")
        except ValueError:
            print(f"{COR_VERMELHO}Por favor, insira um número válido para o ID ou dias.")
    else:
        print(f"{COR_VERMELHO}Não há carros disponíveis para aluguel no momento.")
    
    input(f"{COR_CYAN}\nPressione enter para voltar ao menu.")



def devolver_carro(carros, clientes):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nDevolver um carro:")

    nome_cliente = input(f"{COR_CYAN}Digite seu nome completo: ").strip()
    cnh_cliente = input(f"{COR_CYAN}Digite seu número de CNH: ").strip()

    if cnh_cliente not in clientes:
        input(f"{COR_VERMELHO}Cliente não encontrado. Pressione enter para voltar ao menu.")
        return

    if 'carro_alugado' not in clientes[cnh_cliente]:
        print(f"{COR_VERMELHO}Você não tem um carro alugado.")
        return

    carro_alugado = clientes[cnh_cliente]['carro_alugado']
    print(f"{COR_CYAN}Você alugou o carro {carro_alugado['modelo']}.")
    confirmar = input(f"{COR_AMARELO}Deseja devolver o carro? (S para sim, pressione enter para cancelar): ").strip().lower()

    if confirmar == 's':

        id_carro = carro_alugado['id']
        carros[id_carro]['disponivel'] = True
        print(f"{COR_VERDE}Carro {carro_alugado['modelo']} devolvido com sucesso!")
        
        del clientes[cnh_cliente]['carro_alugado']
        
        salvar_carros(carros)
        salvar_clientes(clientes)
    else:
        print(f"{COR_VERMELHO}Devolução cancelada.")
    
    input(f"{COR_CYAN}\nPressione enter para voltar ao menu.")


def excluir_cliente(clientes, is_funcionario=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nExcluir Cadastro de Cliente:")

    if is_funcionario:
        cnh_cliente = input(f"{COR_CYAN}Digite o número de CNH do cliente a ser excluído: ").strip()
    else:
        nome_cliente = input(f"{COR_CYAN}Digite seu nome completo: ").strip()
        cnh_cliente = input(f"{COR_CYAN}Digite seu número de CNH: ").strip()
    
    if cnh_cliente in clientes:
        info_cliente = clientes[cnh_cliente]
        print(f"{COR_CYAN}Nome: {info_cliente['nome']}")
        print(f"{COR_CYAN}E-mail: {info_cliente['email']}")
        print(f"{COR_CYAN}Telefone: {info_cliente['telefone']}")
        print(f"{COR_CYAN}Data de Nascimento: {info_cliente['data_nascimento']}")
        print(f"{COR_CYAN}Endereço: {info_cliente['endereco']}")
        
        confirmar = input(f"{COR_AMARELO}Tem certeza que deseja excluir o cadastro de {info_cliente['nome']}? (S para sim, qualquer tecla para cancelar): ").strip().lower()
        if confirmar == 's':
            del clientes[cnh_cliente]
            salvar_clientes(clientes)
            print(f"{COR_VERDE}Cadastro de {info_cliente['nome']} excluído com sucesso!")
        else:
            print(f"{COR_VERMELHO}Exclusão cancelada.")
    else:
        print(f"{COR_VERMELHO}Cliente não encontrado.")
    
    input(f"{COR_CYAN}\nPressione Enter para voltar ao menu.")


def validar_telefone(telefone):
    padrao_telefone = r"^\d{9,11}$"
    return re.match(padrao_telefone, telefone)

def validar_data_nascimento(data):
    try:
        dia, mes, ano = map(int, data.split('/'))
        data_nascimento = datetime(ano, mes, dia)
        
        data_atual = datetime.today()
        
        idade = data_atual.year - data_nascimento.year
        if data_atual.month < data_nascimento.month or (data_atual.month == data_nascimento.month and data_atual.day < data_nascimento.day):
            idade -= 1 

        if idade < 18:
            return False
        return True
    except ValueError:
        return False
    
    
def validar_cnh(cnh):
    return len(cnh) == 11 and cnh.isdigit()

def verificar_cnh_existente(clientes, cnh):
    return cnh in clientes

def cadastrar_cliente(clientes):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nCadastro do Cliente:")

    while True:
        nome = input(f"{COR_CYAN}Digite seu nome completo: ").strip()
        if nome:
            break
        else:
            input(f"{COR_VERMELHO}Nome não pode estar vazio. Pressione enter para tentar novamente.")

    while True:
        cnh = input(f"{COR_CYAN}Digite seu número de CNH (11 dígitos): ").strip()
        if validar_cnh(cnh):
            if verificar_cnh_existente(clientes, cnh):
                input(f"{COR_VERMELHO}Já existe um cliente com esse número de CNH. Pressione enter para tentar novamente.")
            else:
                break
        else:
            input(f"{COR_VERMELHO}CNH inválida. A CNH deve ter 11 dígitos. Pressione enter para tentar novamente.")

    while True:
        email = input(f"{COR_CYAN}Digite seu e-mail: ").strip()
        if email:
            break
        else:
            input(f"{COR_VERMELHO}E-mail não pode estar vazio. Pressione enter para tentar novamente.")

    while True:
        telefone = input(f"{COR_CYAN}Digite seu telefone: ").strip()
        if validar_telefone(telefone):
            break
        else:
            input(f"{COR_VERMELHO}Telefone inválido. Deve ter 9 ou 11 dígitos. Pressione enter para tentar novamente.")

    while True:
        data_nascimento = input(f"{COR_CYAN}Digite sua data de nascimento (DD/MM/AAAA): ").strip()
        if validar_data_nascimento(data_nascimento):
            break
        else:
            input(f"{COR_VERMELHO}Data de nascimento inválida ou menor de idade. O formato deve ser DD/MM/AAAA. Pressione enter para tentar novamente.")

    while True:
        endereco = input(f"{COR_CYAN}Digite seu endereço: ").strip()
        if endereco:
            break
        else:
            input(f"{COR_VERMELHO}Endereço não pode estar vazio. Pressione enter para tentar novamente.")

    clientes[cnh] = {'nome': nome, 'email': email, 'telefone': telefone, 'data_nascimento': data_nascimento, 'endereco': endereco}
    salvar_clientes(clientes)

    input(f"{COR_VERDE}Cadastro realizado com sucesso! Pressione Enter para voltar ao menu.")

def alterar_cadastro_cliente(clientes, is_funcionario=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nAlterar Cadastro de Cliente:")

    if is_funcionario:
        cnh_cliente = input(f"{COR_CYAN}Digite o número de CNH do cliente a ser alterado: ").strip()
    else:
        nome_cliente = input(f"{COR_CYAN}Digite seu nome completo: ").strip()
        cnh_cliente = input(f"{COR_CYAN}Digite seu número de CNH: ").strip()

    if cnh_cliente in clientes:
        info_cliente = clientes[cnh_cliente]
        print(f"\n{COR_CYAN}Dados atuais do cliente:")
        print(f"Nome: {info_cliente['nome']}")
        print(f"E-mail: {info_cliente['email']}")
        print(f"Telefone: {info_cliente['telefone']}")
        print(f"Data de Nascimento: {info_cliente['data_nascimento']}")
        print(f"Endereço: {info_cliente['endereco']}")

        print(f"\n{COR_CYAN}O que você deseja alterar?")
        print(f"{COR_AMARELO}1. Nome")
        print(f"{COR_AMARELO}2. E-mail")
        print(f"{COR_AMARELO}3. Telefone")
        print(f"{COR_AMARELO}4. Data de Nascimento")
        print(f"{COR_AMARELO}5. Endereço")
        opcao_alteracao = input(f"{COR_CYAN}Escolha a opção para alterar (1-5): ").strip()

        if opcao_alteracao in ['1', '2', '3', '4', '5']:
            if opcao_alteracao == '1':
                novo_nome = input(f"{COR_CYAN}Digite o novo nome: ").strip()
                if not novo_nome:
                    input(f"{COR_VERMELHO}Nome não pode estar vazio. Pressione enter para voltar ao menu")
                    return
                clientes[cnh_cliente]['nome'] = novo_nome
            elif opcao_alteracao == '2':
                novo_email = input(f"{COR_CYAN}Digite o novo e-mail: ").strip()
                clientes[cnh_cliente]['email'] = novo_email
            elif opcao_alteracao == '3':
                novo_telefone = input(f"{COR_CYAN}Digite o novo telefone: ").strip()
                if not validar_telefone(novo_telefone):
                    input(f"{COR_VERMELHO}Telefone inválido. Deve ter 10 ou 11 dígitos. Pressione enter para voltar ao menu")
                    return
                clientes[cnh_cliente]['telefone'] = novo_telefone
            elif opcao_alteracao == '4':
                nova_data_nascimento = input(f"{COR_CYAN}Digite a nova data de nascimento (DD/MM/AAAA): ").strip()
                if not validar_data_nascimento(nova_data_nascimento):
                    input(f"{COR_VERMELHO}Data de nascimento inválida. O formato deve ser DD/MM/AAAA. Pressione enter para voltar ao menu")
                    return
                clientes[cnh_cliente]['data_nascimento'] = nova_data_nascimento
            elif opcao_alteracao == '5':
                novo_endereco = input(f"{COR_CYAN}Digite o novo endereço: ").strip()
                if not novo_endereco:
                    input(f"{COR_VERMELHO}Endereço não pode estar vazio. Pressione enter para voltar ao menu")
                    return
                clientes[cnh_cliente]['endereco'] = novo_endereco

            salvar_clientes(clientes)
            input(f"{COR_VERDE}Cadastro alterado com sucesso! Pressione Enter para voltar ao menu.")
        else:
            input(f"{COR_VERMELHO}Opção inválida. Alteração cancelada. Pressione enter para voltar ao menu.")
    else:
        input(f"{COR_VERMELHO}Cliente não encontrado. Pressione enter para voltar ao menu.")


def buscar_cliente_por_cnh(clientes):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COR_MAGENTA}\nBuscar Cliente por CNH:")
    cnh_cliente = input(f"{COR_CYAN}Digite o número de CNH do cliente: ").strip()
    
    if cnh_cliente in clientes:
        info_cliente = clientes[cnh_cliente]
        print(f"{COR_CYAN}Nome: {info_cliente['nome']}")
        print(f"{COR_CYAN}E-mail: {info_cliente['email']}")
        print(f"{COR_CYAN}Telefone: {info_cliente['telefone']}")
        print(f"{COR_CYAN}Data de Nascimento: {info_cliente['data_nascimento']}")
        print(f"{COR_CYAN}Endereço: {info_cliente['endereco']}")
    else:
        print(f"{COR_VERMELHO}Cliente não encontrado.")
    
    input(f"{COR_CYAN}\nPressione Enter para voltar ao menu.")


def menu_funcionario():
    carros = carregar_carros()
    clientes = carregar_clientes()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COR_MAGENTA}Menu do Funcionário:")
        print(f"{COR_CYAN}1. Listar carros disponíveis")
        print(f"{COR_CYAN}2. Listar carros alugados")
        print(f"{COR_CYAN}3. Buscar carro por ID")
        print(f"{COR_CYAN}4. Adicionar um novo carro")
        print(f"{COR_CYAN}5. Remover um carro")
        print(f"{COR_CYAN}6. Ver cadastros de clientes")
        print(f"{COR_CYAN}7. Excluir cadastro de cliente")
        print(f"{COR_CYAN}8. Alterar cadastro de cliente")
        print(f"{COR_CYAN}9. Buscar cliente por CNH")
        print(f"{COR_CYAN}10. Sair")
        
        opcao = input(f"{COR_AMARELO}Escolha uma opção: ").strip()

        if opcao == "1":
            listar_carros_disponiveis(carros)
        elif opcao == "2":
            listar_carros_alugados(carros)
        elif opcao == "3":
            buscar_carro(carros)
        elif opcao == "4":
            adicionar_carro(carros)
        elif opcao == "5":
            remover_carro(carros)
        elif opcao == "6":
            for cnh, info in clientes.items():
                print(f"{COR_CYAN}Nome: {info['nome']} | CNH: {cnh} | E-mail: {info['email']}")
            input(f"{COR_CYAN}\nPressione Enter para voltar ao menu.")
        elif opcao == "7":
            excluir_cliente(clientes, is_funcionario=True)
        elif opcao == "8":
            alterar_cadastro_cliente(clientes, is_funcionario=True)
        elif opcao == "9":  
            buscar_cliente_por_cnh(clientes)
        elif opcao == "10":
            print(f"{COR_VERDE}Fechando!")
            break
        else:
            print(f"{COR_VERMELHO}Opção inválida. Tente novamente.")
            
            
def menu_cliente():
    carros = carregar_carros()
    clientes = carregar_clientes()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{COR_MAGENTA}Menu do Cliente:")
        print(f"{COR_CYAN}1. Listar carros disponíveis")
        print(f"{COR_CYAN}2. Buscar carro por ID")
        print(f"{COR_CYAN}3. Alugar um carro")
        print(f"{COR_CYAN}4. Devolver um carro")
        print(f"{COR_CYAN}5. Realizar cadastro")
        print(f"{COR_CYAN}6. Excluir cadastro")
        print(f"{COR_CYAN}7. Alterar meu cadastro")
        print(f"{COR_CYAN}8. Sair")
        
        opcao = input(f"{COR_AMARELO}Escolha uma opção: ").strip()

        if opcao == "1":
            listar_carros_disponiveis(carros)
        elif opcao == "2":
            buscar_carro(carros)
        elif opcao == "3":
            alugar_carro(carros, clientes)
        elif opcao == "4":
            devolver_carro(carros, clientes)
        elif opcao == "5":
            cadastrar_cliente(clientes)
        elif opcao == "6":
            excluir_cliente(clientes)
        elif opcao == "7":
            alterar_cadastro_cliente(clientes)
        elif opcao == "8":
            print(f"{COR_VERDE}Fechando!")
            break
        else:
            print(f"{COR_VERMELHO}Opção inválida. Tente novamente.")

def login():
    while True:
        print(f'{COR_MAGENTA} Bem-vindo a locadora de carros LHN!')
        tipo_usuario = input(f"{COR_VERDE}Digite uma das opções:\n\n {COR_CYAN}1 para Funcionário:\n 2 para Cliente:\n 3 para sair do programa. ").strip()
        
        if tipo_usuario == "1":
            menu_funcionario()
        elif tipo_usuario == "2":
            menu_cliente()
        elif tipo_usuario == "3":
            print("Fechando o programa. Obrigado!")
            break
        else:
            print(f"{COR_VERMELHO}Opção inválida. Tente novamente.")

login()
