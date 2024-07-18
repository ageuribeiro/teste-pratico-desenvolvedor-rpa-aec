from sqlalchemy.exc import OperationalError
from libraries import (
    Flask, render_template, redirect, url_for, request, flash,
    webdriver, Service, By, WebDriverWait, EC,
    time, logging, datetime,
    create_engine, Column, Integer, String, DateTime, declarative_base, sessionmaker
)

# importando a biblioteca Pandas para exportar os dados para um arquivo csv/excel
import pandas as pd


Base = declarative_base()
app = Flask(__name__)
app.secret_key = 'demoqa2024'

# Configuração do processo de logging
logging.basicConfig(filename='automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# Simulação de dados do usuário
valid_username = 'demoqa'
valid_password = 'demoqa2024'

# Caminho para o driver do Chrome
webdriver_service = Service('chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    date_registred = Column(DateTime, default=datetime.datetime.utcnow)

server_name = 'ASUSX512FJ'
database_name = 'book_store_db'
connection_url = f'mssql+pyodbc://{server_name}/{database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# Função que gera o log para os eventos no sistema
def log_event(message, level=logging.INFO):
    if level == logging.INFO:
        logging.info(message)
    elif level == logging.ERROR:
        logging.error(message)

# Tentar conectar ao banco de dados
def connect_with_retry(retries=5, delay=5):
    for attempt in range(retries):
        try:
            connection = engine.connect()
            return connection
        except OperationalError as e:
            log_event(f"Erro ao tentar conectar ao Banco de Dados: {e}", level=logging.ERROR)
            time.sleep(delay)
    raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")

connection = connect_with_retry()

# Rota do endpoint raiz
@app.route('/')
def home():
    return render_template('index.html')

# Rota do endpoint login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']

        if user == valid_username and passw == valid_password:
            flash('Login Bem sucedido!', 'success')
            log_event('Login bem sucedido!')
            time.sleep(10)
            automation()
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas, Por favor tente novamente.', 'danger')
            log_event('Credenciais Inválidas')
            return redirect(url_for('login'))
    return render_template('index.html')

# Inicializando a automação
def run_automation_task(task_function):
    log_event(f'Iniciando automação: {task_function.__name__}')
    try:
        task_function()
    except Exception as e:
        log_event(f'Erro durante a automação: {e}', level=logging.ERROR)
    finally:
        log_event(f'Automação {task_function.__name__} finalizada')

# Automação de elementos
def automate_section(section_name, url_suffix):
    log_event(f'Iniciando automação da seção {section_name}')
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    try:
        driver.get("https://demoqa.com/")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "app")))
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//h5[text()='{section_name}']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        
        list_items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul.menu-list li")))
        for item in list_items:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                item.click()
                time.sleep(10)
                log_event(f'Item de {section_name} clicado com sucesso')
            except Exception as e:
                log_event(f'Erro ao clicar no item de {section_name}: {e}')
    except Exception as e:
        log_event(f'Ocorreu um erro durante a automação de {section_name}: {e}', level=logging.ERROR)
    finally:
        driver.quit()

# Automação da Book Store
def bookstore():
    log_event('Iniciando automação da Book Store')
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    try:
        driver.get("https://demoqa.com/")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "app")))
        
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h5[text()='Book Store Application']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        
        WebDriverWait(driver, 10).until(EC.url_to_be('https://demoqa.com/books'))

        log_event('Página da Book Store acessada com sucesso')
        
        # Aguardar até que a tabela de livros seja visível
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ReactTable")))

        # Localiza todas as linhas dentro de .ReactTable
        rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tr-group .rt-tr")
        books_data = []
        for row in rows:
            columns = row.find_elements(By.CSS_SELECTOR, ".rt-td")
            
            # Certifique-se de que há colunas suficientes para obter os dados
            if len(columns) >= 4:
                title = columns[1].text.strip()
                author = columns[2].text.strip()
                publisher = columns[3].text.strip()
        
                log_event(f"Title: {title}, Author: {author}, Publisher: {publisher}")

                # Salvar os dados no Banco de dados utilizando SQLALchemy
                if title and author and publisher:
                    book = Book(title=title, author=author, publisher=publisher)
                    session.add(book)
                    session.commit()

                # Armazenar os dados em uma lista para exportação
                books_data.append({'Title': title, 'Author': author, 'Publisher': publisher})

        log_event('Livros adicionados à coleção com sucesso')

        # Exportar os dados para CSV e Excel utilizando a biblioteca Pandas
        if books_data:
            df = pd.DataFrame(books_data)
            csv_filename = 'books_data.csv'
            excel_filename = 'books_data.xlsx'

            # Exportando para CSV
            df.to_csv(csv_filename, index=False)
            log_event(f'Dados exportados para {csv_filename}')

            # Exportando para Excel
            df.to_excel(excel_filename, index=False)
            log_event(f'Dados exportados para {excel_filename}')
            
    except Exception as e:
        log_event(f'Ocorreu um erro durante a automação da Book Store: {e}', level=logging.ERROR)
    
    finally:
        driver.quit()
        session.close()

# Função que inicia todas as automações
def automation():
    log_event('Iniciando todas as automações')
    sections = [
        ('Elements','elements'), 
        ('Forms','forms'), 
        ('Alerts, Frame & Windows','alerts'), 
        ('Widgets','widgets'), 
        ('Interactions','interaction'),  # Corrigido o nome da seção 'Interactions'
        ('Book Store Application','books')  # Corrigido o sufixo da URL da Book Store
    ]
    
    for section_name, url_suffix in sections:
        if section_name == 'Book Store Application':
            run_automation_task(bookstore)
        else:
            run_automation_task(lambda: automate_section(section_name, url_suffix))
    log_event('Todas as automações finalizadas')

if __name__ == '__main__':
    app.run(debug=True)


