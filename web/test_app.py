import unittest
from sqlalchemy.exc import OperationalError
from unittest.mock import patch, MagicMock
from app import app, log_event, connect_with_retry, run_automation_task, bookstore
import pandas as pd
import logging

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Home Page', response.data)  # Verifique se o conteúdo esperado está na página

    def test_login_route_success(self):
        response = self.client.post('/login', data={
            'username': 'demoqa',
            'password': 'demoqa2024'
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.assertIn(f'Login Bem sucedido!', response.data)

    def test_login_route_failure(self):
        response = self.client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.assertIn(f"Credenciais inválidas, Por favor tente novamente.", response.data)

    @patch('app.log_event')
    def test_log_event(self, mock_log_event):
        log_event('Test Message', level=logging.INFO)
        mock_log_event.assert_called_once_with('Test Message', level=logging.INFO)

    @patch('app.engine.connect')
    def test_connect_with_retry_success(self, mock_connect):
        mock_connect.return_value = MagicMock()
        connection = connect_with_retry()
        self.assertIsNotNone(connection)

    @patch('app.engine.connect')
    def test_connect_with_retry_failure(self, mock_connect):
        mock_connect.side_effect = OperationalError('Database error', '', '')
        with self.assertRaises(Exception):
            connect_with_retry()

    @patch('app.webdriver.Chrome')
    @patch('app.WebDriverWait')
    @patch('app.EC')
    def test_run_automation_task(self, mock_ec, mock_webdriver_wait, mock_chrome):
        mock_task = MagicMock()
        run_automation_task(mock_task)
        mock_task.assert_called_once()

    @patch('app.webdriver.Chrome')
    @patch('app.WebDriverWait')
    @patch('app.EC')
    def test_bookstore(self, mock_ec, mock_webdriver_wait, mock_chrome):
        mock_chrome_instance = MagicMock()
        mock_chrome.return_value = mock_chrome_instance
        mock_webdriver_wait.return_value.until.return_value = MagicMock()
        mock_webdriver_wait.return_value.until.return_value.find_elements.return_value = []

        with patch('app.session') as mock_session:
            bookstore()
            # Verifica se os dados foram salvos no banco de dados
            mock_session.add.assert_called()
            mock_session.commit.assert_called()

    @patch('app.pd.DataFrame')
    def test_export_data(self, mock_dataframe):
        mock_dataframe.return_value = MagicMock()
        mock_dataframe.return_value.to_csv = MagicMock()
        mock_dataframe.return_value.to_excel = MagicMock()

        bookstore()
        # Verifica se o método to_csv e to_excel foram chamados
        mock_dataframe.return_value.to_csv.assert_called()
        mock_dataframe.return_value.to_excel.assert_called()

if __name__ == '__main__':
    unittest.main()
