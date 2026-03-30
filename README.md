# PyPlatzi

Una pequeña herramienta y librería en Python para interactuar con la API de Platzi. Su función principal actualmente es listar y exportar los cursos que has aprobado.

## Instalación

```bash
pip install git+https://github.com/CalumRakk/pyplatzi
```

## Autenticación (Configuración de Cookies)

Para que `pyplatzi` pueda consultar tus datos privados, necesitas proporcionar tus cookies de sesión. Sigue estos pasos para obtenerlas correctamente:

1. **Instala la extensión**: En tu navegador (Chrome o Edge), instala la extensión [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc). 
   * *Nota: Asegúrate de usar esta versión "LOCALLY" por seguridad, ya que no envía tus datos a servidores externos.*
2. **Inicia sesión**: Ve a [platzi.com](https://platzi.com) e inicia sesión con tu cuenta de forma normal.
3. **Exporta las cookies**:
   * Haz clic en el icono de la extensión en la barra de herramientas.
   * Asegúrate de estar en la pestaña de Platzi.
   * Haz clic en **"Export"** (asegúrate de que el formato sea **Netscape/Mozilla**).
4. **Guarda el archivo**: Guarda el archivo generado como `platzi_cookies.txt` en la carpeta de este proyecto.

> [!IMPORTANT]
> **Seguridad**: Nunca compartas tu archivo de cookies con nadie. Este archivo contiene tus credenciales de acceso y permite entrar a tu cuenta de Platzi.


## Uso del CLI

Una vez instalado, tendrás disponible el comando `pyplatzi`.

### Listar cursos en la terminal
```bash
pyplatzi my-courses --cookies platzi_cookies.txt
```

### Exportar cursos a un archivo JSON
```bash
pyplatzi my-courses --cookies platzi_cookies.txt --output mis_cursos.json
```

## Uso como Librería

Si prefieres usarlo en tu propio código:

```python
from pyplatzi import PlatziClient

client = PlatziClient(cookies_path="platzi_cookies.txt")
data = client.get_all_approved_courses()

for course in data.courses:
    print(f"Curso: {course.title} - Aprobado el: {course.diploma.approved_date}")
```
