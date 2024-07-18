from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

url = "https://demoqa.com/books"
options = webdriver.ChromeOptions()
webdriver_service = Service("chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=webdriver_service, options=options)
rows = driver.find_elements(By.CSS_SELECTOR, 'div.rt-tbody .rt-tr-group')

#table
table_data = []

for row in rows:
    row_data = []

    cells = row.find_elements(By.CSS_SELECTOR, 'div.rt-td')
    for cell in cells:
        row_data.append(cell.text)
    table_data.append(row_data)

# Mostrar os dados da tabela
for row in table_data:
    print(row)

# fechar o driver
driver.quit()
