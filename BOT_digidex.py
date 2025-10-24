from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, time
import sqlite3

def salvar_dados(dados):
    """
    Função para salvar os dados do digimon na Digidex
    Parameters:
    -----------
    dados (list): Lista com os dados do digimon
    -----------
    """
    try:
        # Conectar (cria o arquivo se não existir)
        conn = sqlite3.connect('digidex.db')
        cursor = conn.cursor()

        # Criar tabela se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS digimon (
                nome TEXT PRIMARY KEY,
                level TEXT,
                tipo TEXT,
                atributo TEXT,
                movimento TEXT
            )
        ''')

        # Inserir ou atualizar dados
        cursor.execute('''
            INSERT INTO digimon (nome, level, tipo, atributo, movimento)
            VALUES (:nome, :level, :tipo, :atributo, :movimento)
            ON CONFLICT(nome) DO UPDATE SET
                level = excluded.level,
                tipo = excluded.tipo,
                atributo = excluded.atributo,
                movimento = excluded.movimento
        ''', {
            "nome": str(dados[0]),
            "level": str(dados[1]),
            "tipo": str(dados[2]),
            "atributo": str(dados[3]),
            "movimento": str(dados[4]),
        })

        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao salvar dados: {e}")

    finally:
        if conn:
            conn.close()

def pegar_dados(nome):
    """
    Função para pegar os dados do digimon na Digidex
    Parameters:
    -----------
    nome (str): Nome do digimon
    -----------
    """
    gc.execute_script("document.body.style.zoom='25%'")
    
    # Pegando o layout dos valores
    valores_layout = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/section/div/div[3]/div[2]')
    
    # Declarando lista de atributos
    atributos = []
    
    # Pegando os atributos do digimon
    atributos.append(nome)
    for i in range(0,4):
        atributo = valores_layout.find_element(By.XPATH, f'./dl[{i+1}]/dd').text
        atributos.append(atributo)
    print(atributos)
    print(1)
    
    salvar_dados(atributos)

def pegando_digimon(nome_digimon):
    
    """
    Função para pegar o digimon na Digidex
    Parameters:
    -----------
    nome_digimon (str): Nome do digimon a ser pesquisado
    -----------
    """
    
    # Grid de itens
    grid = gc.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[2]/div/ul")
    # Pegando 
    itens = grid.find_elements(By.CSS_SELECTOR, "ul li")
    
    # Percorrendo os itens do grid ate achar o digimon pesquisado
    for item in itens:
        # Pegando o nome do digimon do item
        nome = item.find_element(By.XPATH, './a/div[2]/p').text
        # Comparando o nome do digimon com o nome pesquisado
        if nome.lower() == nome_digimon.lower():
            item.click()
            sleep(1)
            # Capitalizando o nome do digimon
            nome = nome.capitalize()
            
            pegar_dados(nome)
            
            # Fechando o navegador
            gc.quit()
            break

def pegando_digimons():
    
    """
    Função para pegar os digimons na Digidex
    """
    
    abrir_navegador("https://digimon.net/reference_en/")
    sleep(3)
      
    grid = gc.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[2]/div")
    # Pegando 
    itens = grid.find_elements(By.CSS_SELECTOR, "ul li")
    
    # Percorrendo os itens do grid ate achar o digimon pesquisado
    for item in range(len(itens)):
        # Pegando o nome do digimon do item
        grid = gc.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[2]/div")
        # Pegando 
        itens = grid.find_elements(By.CSS_SELECTOR, "ul li")
        item_atual = itens[item].find_element(By.XPATH, './a/div[2]/p')
        nome = item_atual.text
        # Comparando o nome do digimon com o nome pesquisado
        url_anterior= gc.current_url
        # Capitalizando o nome do digimon
        nome = nome.capitalize()
        print(nome)
        item_atual.click()
        sleep(1)
        pegar_dados(nome)
        
        gc.get(url_anterior)
        gc.execute_script("document.body.style.zoom='25%'")
        sleep(3)
        
    gc.quit()
    
def abrir_navegador(url):
    
    """
    Função para abrir o navegador
    Parameters:
    -----------
    url (str): URL para abrir no navegador
    -----------
    """
    
    global gc
    option = Options()
    option.add_argument("enable-automation")
    option.add_argument("--start-maximized")
    gc = webdriver.Chrome(options=option)

    gc.get(url)
    sleep(5)
    gc.execute_script("document.body.style.zoom='25%'")

def pesquisar(digimon):
    """
    Função para pesquisar o digimon na Digidex
    
    Parameters:
    -----------
    digimon (int): 0 - Agumon | 1 - Gabumon | 2 - Patamon | 3 - Biyomon | 4 - Tentomon | 5 - Gomamon | 6 - Palmon | 7 - Gatomon
    -----------
    """
    global gc

    abrir_navegador("https://digimon.net/reference_en/")

    # Pesquisando no input pesquisar
    
    input_pesquisar = gc.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/form/div[1]/dl/dd/input")
    input_pesquisar.click()
    input_pesquisar.send_keys(digimon, Keys.ENTER)

    pegando_digimon(digimon)

def menu2():
    while True:
        print("========= Digidex =========")
        print("1 - varrer digidex")
        print("2 - pesquisar digimon")
        print("3 - Sair")
        print("===========================")
        opcao = input("Escolha uma opção: ")
        
        match int(opcao):
            case 1:
                abrir_navegador("https://digimon.net/reference_en/")
                pegando_digimons()
                return True
            case 2:
                pesquisar(input("Escolha um digimon: "))
                return True
            case 3:
                print("Saindo...")
                return False
            case _: 
                print("Opção inválida!!")

def menu():
    
    """
    Menu De interação Da Digidex
    """
    
    while True:
        print("========= Digidex =========")
        print("1 - Agumon")
        print("2 - Gabumon")
        print("3 - Patamon")
        print("4 - Biyomon")
        print("5 - Tentomon")
        print("6 - Gomamon")
        print("7 - Palmon")
        print("8 - Gatomon")
        print('9 - printar')
        print("10 - Sair")
        print("===========================")
        opcao = input("Escolha um digimon: ")
        match opcao:
            case '1':
                pesquisar(0)
            case '2':
                pesquisar(1)
            case '3':
                pesquisar(2)
            case '4':
                pesquisar(3)
            case '5':
                pesquisar(4)
            case '6':
                pesquisar(5)
            case '7':
                pesquisar(6)
            case '8':
                pesquisar(7)
            case '9':
                print("printando...")
            case '10':
                print("encerrando...")
                break
            case _:
                print("valor inválido!!")
        
"""
MAIN
"""

menu2()