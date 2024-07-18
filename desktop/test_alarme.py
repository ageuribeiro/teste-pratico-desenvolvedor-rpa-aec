import unittest
from unittest.mock import patch, MagicMock
import time 
import pyautogui
import pygetwindow as gw
from alarme import open_alarm_app, create_alarm, wait


class TestAlarmFunctions(unittest.TestCase):

    @patch('pygetwindow.getWindowsWithTitle')
    @patch('pyautogui.press')
    @patch('pyautogui.write')
    @patch('pyautogui.hotkey')
    def test_open_alarm_app_existing_window(self, mock_hotkey, mock_write, mock_press, mock_getWindowsWithTitle):
        # Simular que o aplicativo de alarmes já está aberto
        mock_getWindowsWithTitle.return_value = [MagicMock()]
        open_alarm_app()
        mock_getWindowsWithTitle.assert_called_once_with('Alarmes e Relógio')
        mock_hotkey.assert_not_called()  # Não deve pressionar 'win' para abrir o aplicativo


    @patch('pygetwindow.getWindowsWithTitle')
    @patch('pyautogui.press')
    @patch('pyautogui.write')
    @patch('pyautogui.hotkey')
    def test_open_alarm_app_new_window(self, mock_hotkey, mock_write, mock_press, mock_getWindowsWithTitle):
        # Simular que o aplicativo de alarmes não está aberto
        mock_getWindowsWithTitle.return_value = []
        open_alarm_app()
        mock_getWindowsWithTitle.assert_called_once_with('Alarmes e Relógio')
        mock_hotkey.assert_called_with('win')
        mock_press.assert_called_with('enter')


    @patch('pyautogui.press')
    @patch('pyautogui.write')
    @patch('pyautogui.hotkey')
    def test_create_alarm(self, mock_hotkey, mock_write, mock_press):
        # Testar a criação de um alarme
        create_alarm("08", "00", "YES", "Test Message", "week", "Jingle", "10")
        mock_write.assert_any_call("08")
        mock_write.assert_any_call("00")
        mock_write.assert_any_call("Test Message")
        mock_hotkey.assert_called_with('shift', 'tab')


    @patch('pyautogui.press')
    @patch('pyautogui.write')
    def test_wait_function(self, mock_write, mock_press):
        # Testar a função wait para garantir que ela realmente pausa a execução
        start_time = time.time()
        wait(2)
        end_time = time.time()
        self.assertGreaterEqual(end_time - start_time, 2)

if __name__ == '__main__':
    unittest.main()