from http.cookiejar import MozillaCookieJar
from pathlib import Path

import requests

from pyplatzi.constants import BASE_API_URL, HEADERS


def parser_cookies(path:Path):    
    cj = MozillaCookieJar()
    if not path.exists():
        raise FileNotFoundError(f"El archivo de cookies no existe: {path}")

    cj.load(path.as_posix(), ignore_discard=True, ignore_expires=True)

    cookies={}
    for cookie in cj:
        cookies[cookie.name]=cookie.value

    return cookies


def get_access(cookies_path:Path):
    cookies= parser_cookies(cookies_path)

    response = requests.get(f'{BASE_API_URL}/api/v5/users/credentials/', cookies=cookies, headers=HEADERS)
    response.raise_for_status()
    data= response.json()
    if data["ok"]=="Token generated":
        return data["token"]["access"]
    raise Exception("Error al obtener el token de acceso")