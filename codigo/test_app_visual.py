"""Comprueba la conexión HTTP real y las entradas de la aplicación local."""
from http.server import ThreadingHTTPServer
import json
from threading import Thread
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app_visual import Handler


class QuietHandler(Handler):
    def log_message(self, format, *args):
        """Silencia el diagnóstico HTTP para conservar legible la salida de unittest."""
        pass


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicia un servidor HTTP real en un puerto local libre para las pruebas."""
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        """Detiene el servidor, libera su puerto y espera al hilo de pruebas."""
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, path, payload=None, **headers):
        """Envía una petición real y devuelve estado y cuerpo, también para respuestas de error."""
        data = None if payload is None else payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        request = Request(self.url + path, data=data, headers=headers)
        try:
            with urlopen(request, timeout=8) as response:
                return response.status, response.read()
        except HTTPError as error:
            return error.code, error.read()

    def example(self):
        """Obtiene del servidor la carga E2 para construir una comparación reproducible."""
        status, body = self.request('/api/scenarios')
        self.assertEqual(status, 200)
        case = json.loads(body)[1]
        return dict(processes=case['processes'], quantum=case['quantum'])

    def test_page_and_presets(self):
        """Comprueba acceso a la página y presencia de los cinco escenarios."""
        status, body = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'Laboratorio de', body)
        status, body = self.request('/api/scenarios')
        self.assertEqual(len(json.loads(body)), 5)

    def test_manual_example_over_http(self):
        """Verifica por HTTP las esperas manuales de P2 y conservación de 18 unidades CPU."""
        status, body = self.request('/api/compare', self.example())
        self.assertEqual(status, 200)
        a, b = json.loads(body)['results']
        self.assertEqual(a['processes'][1]['waiting'], 11)
        self.assertEqual(b['processes'][1]['waiting'], 2)
        self.assertEqual(a['metrics']['busy_time'], 18)
        self.assertEqual(b['metrics']['busy_time'], 18)

    def test_zero_quantum_is_rejected(self):
        """Comprueba el rechazo HTTP de quantum cero."""
        data = self.example()
        data['quantum'] = 0
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_duplicate_pid_is_rejected(self):
        """Comprueba que dos procesos con igual PID no se admiten."""
        data = self.example()
        data['processes'][1]['pid'] = 1
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_fractional_input_is_rejected(self):
        """Rechaza CPU fraccionaria cuando el modelo requiere tiempos enteros."""
        data = self.example()
        data['processes'][0]['cpu'] = 1.5
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_unknown_path_does_not_serve_files(self):
        """Verifica que rutas arbitrarias no expongan archivos del proyecto."""
        self.assertEqual(self.request('/models.py')[0], 404)

    def test_foreign_origin_is_rejected(self):
        """Rechaza una solicitud procedente de un origen distinto del servidor local."""
        self.assertEqual(self.request('/api/compare', self.example(), Origin='https://example.org')[0], 403)

    def test_io_input_is_preserved(self):
        """Comprueba bloqueo de cuatro unidades y transiciones BLOQUEADO para E4."""
        status, body = self.request('/api/scenarios')
        case = json.loads(body)[3]
        status, body = self.request('/api/compare', dict(processes=case['processes'], quantum=case['quantum']))
        self.assertEqual(status, 200)
        for r in json.loads(body)['results']:
            self.assertEqual(r['processes'][0]['blocked'], 4)
            self.assertIn('BLOQUEADO', [e['state'] for e in r['events']])

    def test_invalid_encoding_returns_readable_error(self):
        """Comprueba que bytes no UTF-8 reciben un error JSON en vez de cortar la conexión."""
        status, body = self.request('/api/compare', b'\xff')
        self.assertEqual(status, 400)
        self.assertIn('UTF-8', json.loads(body)['error'])

    def test_excessive_cpu_is_rejected_before_simulation(self):
        """Rechaza una carga visual que supera el límite total de CPU."""
        payload = dict(quantum=1, processes=[dict(pid=i, arrival=0, cpu=1000, io=[]) for i in (1, 2, 3)])
        status, body = self.request('/api/compare', payload)
        self.assertEqual(status, 400)
        self.assertIn('2000', json.loads(body)['error'])

    def test_script_and_stylesheet_are_served(self):
        """Verifica que JavaScript y CSS separados sean accesibles como recursos explícitos."""
        for path, expected in [('/interfaz.js', b'function render'), ('/estilos.css', b':root')]:
            with self.subTest(path=path):
                status, body = self.request(path)
                self.assertEqual(status, 200)
                self.assertIn(expected, body)

    def test_missing_resource_returns_readable_error(self):
        """Comprueba respuesta JSON 500 si falta un archivo necesario para la interfaz."""
        with TemporaryDirectory() as directory, patch('app_visual.ROOT', Path(directory)):
            status, body = self.request('/')
            self.assertEqual(status, 500)
            self.assertIn('recurso', json.loads(body)['error'])


if __name__ == '__main__':
    unittest.main()
