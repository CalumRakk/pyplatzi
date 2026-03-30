import random
import time
from pathlib import Path
from typing import Optional

import requests
from schemas import Response
from utils import get_access

access = get_access(Path(r"D:\github Leo\pyplatzi\platzi.com_cookies.txt"))

headers = {
    'accept': '*/*',
    'accept-language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,es-CO;q=0.5',
    'api-authorization': 'Bearer ' + access,
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://platzi.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
    'x-csrftoken': '',
    'x-requested-with': 'XMLHttpRequest',
}

def get_data(cursor:int)-> Optional[Response]:
    params = {
        'page': cursor,
        'page_size': '50',
        'only_approved': 'true',
    }
    response = requests.get('https://api.platzi.com/profile/v1/courses/', params=params, headers=headers)
    response.raise_for_status()

    data= response.json()
    if data.get("data") is None:
        return None 
       
    return  Response(**data)

response= get_data(1)
if response is None:
    raise ValueError("No se pudo obtener la información de los cursos aprobados.")

current_page= 1
total_pages = response.metadata.pages
approved_courses= response.data.approved_courses

courses= []
courses.extend(response.data.courses)

while current_page <= total_pages:
    current_page += 1
    response= get_data(current_page)
    if response is None:
        print(f"No se pudo obtener la información de los cursos aprobados para la página {current_page}.")
        continue

    courses.extend(response.data.courses)

    time.sleep(random.randint(1, 3))

print(courses)

