from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep, time
import sqlite3

def menu():
    print("========= Digidex =========")
    print("1 - Agumon")
    print("2 - Gabumon")
    print("3 - Patamon")
    print("4 - Biyomon")
    print("5 - Tentomon")
    print("6 - Gomamon")
    print("7 - Palmon")
    print("8 - Gatomon")
    print("9 - Sair")
    print("===========================")
    opcao = input("Escolha um digimon: ")
    
    match int(opcao):
        case 1:
            pesquisar_digimon(0)
            return True
        case 2:
            pesquisar_digimon(1)
            return True
        case 3:
            pesquisar_digimon(2)
            return True
        case 4:
            pesquisar_digimon(3)
            return True
        case 5:
            pesquisar_digimon(4)
            return True
        case 6:
            pesquisar_digimon(5)
            return True
        case 7:
            pesquisar_digimon(6)
            return True
        case 8:
            pesquisar_digimon(7)
            return True
        case 9:
            print("Saindo...")
            return False
        case _: 
            print("Opção inválida!!")

def pesquisar_digimon(digimon):
    option = Options()
    option.add_argument("enable-automation")
    option.add_argument("--start-maximized")
    option.add_argument(r"--user-data-dir=C:\Users\Felipe\AppData\Local\Microsoft\Edge\User Data\Default")
    option.add_argument("--profile-directory=Profile2")
    global gc
    gc = webdriver.Edge(options=option)
    lista_digimon = ['Agumon', 'Gabumon', 'Patamon','Biyomon','Tentomon','Gomamon','Palmon','Gatomon']
    gc.get('https://digimon.net/reference_en/')
    sleep(5)
    gc.execute_script("document.body.style.zoom='25%'")
    search_box = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/form/div[1]/dl/dd/input')
    search_box.clear()
    search_box.send_keys(lista_digimon[digimon])
    search_box.send_keys(Keys.ENTER)
    sleep(3)
    grid = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div')
    itens = grid.find_elements(By.CSS_SELECTOR, "ul li")
    for item in itens:
        nome = item.get_attribute('id')
        if nome.lower() == lista_digimon[digimon].lower():
            item.click()
            sleep(5)
            detalhes = pegando_detalhes()
            dados = {
                "nome": lista_digimon[digimon],
                "detalhes": detalhes
            }
            salvar_dados(dados)
            return 
    gc.quit()
    return

def pegando_detalhes():
    level = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/section/div/div[3]/div[2]/dl[1]/dd').text
    tipo = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/section/div/div[3]/div[2]/dl[2]/dd').text
    atributo = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/section/div/div[3]/div[2]/dl[3]/dd').text
    movimento = gc.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div/section/div/div[3]/div[2]/dl[4]/dd').text
    return {
        "level": level,
        "tipo": tipo,
        "atributo": atributo,
        "movimento": movimento
    }

def salvar_dados(dados):
    # Conectar (cria o arquivo se não existir)
    conn = sqlite3.connect('digidex.db')
    cur = conn.cursor()
    # Criar tabela se não existir
    cur.execute('''
        CREATE TABLE IF NOT EXISTS digimon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            level TEXT,
            tipo TEXT,
            atributo TEXT,
            movimento TEXT
        )
    ''')
    # Inserir dados
    detalhes = dados.get('detalhes', {}) if isinstance(dados, dict) else {}
    cur.execute(
        'INSERT INTO digimon (nome, level, tipo, atributo, movimento) VALUES (?, ?, ?, ?, ?)',
        (
            dados.get('nome'),
            detalhes.get('level'),
            detalhes.get('tipo'),
            detalhes.get('atributo'),
            detalhes.get('movimento')
        )
    )
    conn.commit()
    conn.close()
    # Fechar o browser se aberto
    try:
        gc.quit()
    except Exception:
        pass

boolenao = True
while boolenao:
   boolenao = menu()