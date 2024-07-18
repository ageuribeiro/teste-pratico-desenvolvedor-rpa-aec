import pyautogui
import pygetwindow as gw
import time

# Função para abrir o aplicativo "Alarmes e Relógio"
def open_alarm_app():
    try:
        # Verificar se a janela já está aberta
        windows = gw.getWindowsWithTitle('Alarmes e Relógio')      
        if windows:
            print("Alternando para o aplicativo de alarmes...")
            for window in windows:
                window.activate()
            time.sleep(3)  # Aguardar 3 segundos para garantir que a janela está em foco
        else:
            print("Abrindo o aplicativo de alarmes...")
            pyautogui.press('win')  # Abre o menu Iniciar
            time.sleep(3)
            pyautogui.write('Alarme')  # Digita 'Alarme' para procurar o aplicativo
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)  # Espera o aplicativo abrir

        # Navegar para a área de Alarmes
        pyautogui.press('down', presses=2)  # Move para a área de Alarmes
        time.sleep(2)
        pyautogui.press('enter')  # Entrar na tela de adição de alarmes
        time.sleep(2)
        pyautogui.press('tab', presses=3)  # Posicionar a seleção no botão para criar novo alarme
        time.sleep(2)

    except Exception as e:
        print(f"Erro ao abrir o aplicativo de alarmes: {e}")

# Função auxiliar para esperar um tempo
def wait(seconds):
    time.sleep(seconds)

# Função para criar um alarme
def create_alarm(hour, minutes, repeat, message, week_days, jingle, repeat_time):
    try:
        pyautogui.press('enter')  # Entrar na tela de configuração de novo alarme
        wait(2)
        pyautogui.write(hour)  # Escrever a hora do alarme
        wait(2)
        pyautogui.press('tab')  # Selecionar o campo de minutos
        wait(2)
        pyautogui.write(minutes)  # Escrever o minuto do Alarme
        wait(2)
        pyautogui.press('tab')  # Selecionar o campo de Mensagem
        pyautogui.write(message)  # Escrever a mensagem do Alarme
        wait(2)
        pyautogui.press('tab')  # Selecionar o input checkbox

        if repeat == 'YES':  # Verificar se é necessário repetir o evento de alarme
            pyautogui.press('space')  # Seleciona o checkbox para ativar a repetição
            wait(2)
            pyautogui.press('tab')  # Seleciona a lista de dias
            wait(2)
            pyautogui.press('tab')
            if week_days == 'week':
                for _ in range(5):
                    pyautogui.press('right')
                    pyautogui.press('space')
                    wait(1)
            elif week_days == 'weekend':
                pyautogui.press('space')
                wait(1)
                pyautogui.press('right', presses=6)
                pyautogui.press('space')
                wait(1)
        else:  # Caso contrário, seleciona só os dias da semana
            pyautogui.press('tab')  # Ignorar a repetição
            if week_days == 'week':
                for _ in range(5):
                    pyautogui.press('right')
                    pyautogui.press('space')
                    wait(1)
            elif week_days == 'weekend':
                pyautogui.press('space')
                wait(1)
                pyautogui.press('right', presses=6)
                pyautogui.press('space')
                wait(1)

        wait(1)
        pyautogui.press('tab')  # Seleciona a lista suspensa para escolher um som de alarme
        wait(1)
        pyautogui.press('down', presses=3 if jingle == "Jingle" else 0)  # Seleciona o Jingle da lista
        wait(2)
        pyautogui.press('tab')  # Seleciona a lista suspensa para escolher o tempo do alarme
        wait(2)
        pyautogui.write(repeat_time)  # Escolher duração do alarme
        wait(2)
        pyautogui.press('tab')  # Selecionar o botão Salvar
        wait(2)
        pyautogui.press('enter')  # Salvar o Alarme
        wait(2)
        pyautogui.hotkey('shift', 'tab')  # Retornar ao último passo após salvar o alarme

    except Exception as e:
        print(f"Erro ao criar o alarme: {e}")

# Função principal para abrir o aplicativo e criar alarmes
def main():
    open_alarm_app()
    
    alarms = [
        ("08", "00", "NOT", "Tenha um excelente dia de trabalho!", "week", "None", "5"),
        ("07", "45", "YES", "Curtir o Final de Semana!", "weekend", "Jingle", "30")
    ]
    
    for alarm in alarms:
        create_alarm(*alarm)

if __name__ == "__main__":
    main()
