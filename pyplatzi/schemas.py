


from pydantic import BaseModel


class Diploma(BaseModel):
    diploma_url: str # Url del detalle del diploma
    diploma_image: str # Imagen del diploma
    approved_date: str # Fecha de aprobación del curso

    # URLs para compartir en redes
    twitter_share: str 
    facebook_share: str
    linkedin_share: str
    download_url: dict
    is_paywall_enabled: bool


class Course(BaseModel):
    id: int
    title: str
    badge_url: str # url del icono del curso?
    slug: str
    progress:int
    diploma: Diploma


class Data(BaseModel):
    approved_courses: int
    courses: list[Course]


class Metadata(BaseModel):
    count: int
    current_page: int
    pages: int


class Response(BaseModel):
    data: Data
    metadata: Metadata
