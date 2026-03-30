

import logging
import random
import time
from pathlib import Path

import requests

from pyplatzi.constants import BASE_API_URL, HEADERS
from pyplatzi.schemas import MyCourses, Response
from pyplatzi.utils import get_access

logger= logging.getLogger(__name__)


class PlatziClient:
    def __init__(self, cookies_path: str | Path):
        
        self.token= get_access(Path(cookies_path))

        self.session= requests.Session()
        self.session.headers.update(HEADERS)
        self.session.headers.update({'api-authorization': 'Bearer ' + self.token})
    
    def fetch_courses_pages(self, page:int=1, page_size:int=50, only_approved:bool=True):
        params = {
            'page': page,
            'page_size': page_size,
            'only_approved': only_approved,
        }

        url= f"{BASE_API_URL}/profile/v1/courses/"

        logger.debug(f"Petición API: Página {page}")

        response = self.session.get(url, params=params)

        response.raise_for_status()

        data= response.json()
        if bool(data.get("data")) is False:
            return None 
        
        return  Response(**data)

    def get_all_approved_courses(self)->MyCourses:
        
        all_courses= []
        current_page= 1

        initial_data= self.fetch_courses_pages(page=current_page)
        
        if initial_data is None:
            return MyCourses(approved_courses=0, courses=[])
        
        logger.info(f"Iniciando descarga de cursos. Total páginas estimadas: {initial_data.metadata.pages}")

        all_courses.extend(initial_data.data.courses)
        total_pages = initial_data.metadata.pages
        approved_courses = initial_data.data.approved_courses
        while current_page <= total_pages:
            current_page += 1

            logger.info(f"Procesada página {current_page}/{total_pages} ({len(all_courses)} cursos acumulados)")

            data= self.fetch_courses_pages(page=current_page)
            if data is None:
                logger.warning(f"No se pudo obtener la información de los cursos aprobados para la página {current_page}.")
                continue

            all_courses.extend(data.data.courses)

            wait_time = random.randint(1, 3)
            logger.debug(f"Esperando {wait_time}s para evitar rate-limit...")
            time.sleep(wait_time)

        logger.info(f"Carga finalizada: {len(all_courses)} cursos obtenidos.")
        return MyCourses(approved_courses=approved_courses, courses=all_courses)