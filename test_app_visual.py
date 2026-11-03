"""Comprueba la conexión HTTP real y las entradas de la aplicación local."""
from http.server import ThreadingHTTPServer
import json
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app_visual import Handler


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, path, payload=None, **headers):
        data = None if payload is None else json.dumps(payload).encode()
        request = Request(self.url + path, data=data, headers=headers)
        try:
            with urlopen(request, timeout=8) as response:
                return response.status, response.read()
        except HTTPError as error:
            return error.code, error.read()

    def example(self):
        status, body = self.request('/api/scenarios')
        self.assertEqual(status, 200)
        case = json.loads(body)[1]
        return dict(processes=case['processes'], quantum=case['quantum'])

    def test_page_and_presets(self):
        status, body = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'Laboratorio de', body)
        status, body = self.request('/api/scenarios')
        self.assertEqual(len(json.loads(body)), 5)

    def test_manual_example_over_http(self):
        status, body = self.request('/api/compare', self.example())
        self.assertEqual(status, 200)
        a, b = json.loads(body)['results']
        self.assertEqual(a['processes'][1]['waiting'], 11)
        self.assertEqual(b['processes'][1]['waiting'], 2)
        self.assertEqual(a['metrics']['busy_time'], 18)
        self.assertEqual(b['metrics']['busy_time'], 18)

    def test_zero_quantum_is_rejected(self):
        data = self.example()
        data['quantum'] = 0
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_duplicate_pid_is_rejected(self):
        data = self.example()
        data['processes'][1]['pid'] = 1
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_fractional_input_is_rejected(self):
        data = self.example()
        data['processes'][0]['cpu'] = 1.5
        self.assertEqual(self.request('/api/compare', data)[0], 400)

    def test_unknown_path_does_not_serve_files(self):
        self.assertEqual(self.request('/models.py')[0], 404)

    def test_foreign_origin_is_rejected(self):
        self.assertEqual(self.request('/api/compare', self.example(), Origin='https://example.org')[0], 403)

    def test_io_input_is_preserved(self):
        status, body = self.request('/api/scenarios')
        case = json.loads(body)[3]
        status, body = self.request('/api/compare', dict(processes=case['processes'], quantum=case['quantum']))
        self.assertEqual(status, 200)
        for r in json.loads(body)['results']:
            self.assertEqual(r['processes'][0]['blocked'], 4)
            self.assertIn('BLOQUEADO', [e['state'] for e in r['events']])


if __name__ == '__main__':
    unittest.main()
