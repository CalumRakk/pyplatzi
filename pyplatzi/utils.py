from http.cookiejar import MozillaCookieJar
from pathlib import Path

import requests

HEADERS = {
    'accept': '*/*',
    'accept-language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,es-CO;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
}

def parser_cookies(path:Path):    
    cj = MozillaCookieJar()

    cj.load(path.as_posix(), ignore_discard=True, ignore_expires=True)

    cookies={}
    for cookie in cj:
        cookies[cookie.name]=cookie.value

    return cookies


def get_access(cookies_path:Path):
    cookies= parser_cookies(cookies_path)

    response = requests.get('https://platzi.com/api/v5/users/credentials/', cookies=cookies, headers=HEADERS)
    response.raise_for_status()
    data= response.json()
    if data["ok"]=="Token generated":
        return data["token"]["access"]
    raise Exception("Error al obtener el token de acceso")