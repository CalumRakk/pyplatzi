import logging
from http.cookiejar import MozillaCookieJar
from pathlib import Path

import requests

from pyplatzi.constants import BASE_API_URL, HEADERS

logger = logging.getLogger(__name__)

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
    logger.info(f"Intentando obtener token de acceso con cookies de: {cookies_path.name}")

    response = requests.get(f'{BASE_API_URL}/api/v5/users/credentials/', cookies=cookies, headers=HEADERS)
    response.raise_for_status()
    data= response.json()
    if data["ok"]=="Token generated":
        logger.info("Token de acceso generado correctamente.")
        return data["token"]["access"]
    
    logger.error("No se pudo generar el token desde la API.")
    raise Exception("Error al obtener el token de acceso")