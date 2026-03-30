
from pyplatzi import PlatziClient

client= PlatziClient(cookies_path=r"platzi.com_cookies.txt")

miruta= client.get_miruta()

for course in miruta.courses:
    print(f"{course.title} - {course.diploma.approved_date}")