import ssl
import subprocess
import urllib.request
from pathlib import Path


_path_here = Path(__file__).parent
_path_cert = _path_here / 'webhook_cert.pem'
_path_pkey = _path_here / 'webhook_pkey.pem'


def get_ssl_context(ip=None):
    cert, pkey = get_cert(ip)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(cert, pkey)
    return ssl_context


def get_cert(ip=None):
    if not _path_cert.exists():
        ip = ip or get_ip()
        cmd(f'openssl genrsa -out {_path_pkey} 2048')
        cmd(f'openssl req -new -x509 -days 3650 -key {_path_pkey} -out {_path_cert} -subj /commonName={ip}')
    return _path_cert, _path_pkey


def get_ip():
    with urllib.request.urlopen("http://api.ipify.org/") as response:
        return response.read().decode('ascii')


def cmd(t):
    assert subprocess.call(t, shell=True) == 0


if __name__ == '__main__':
    print(get_cert(ip="0.0.0.0"))
