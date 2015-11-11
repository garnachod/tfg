# Documentación de I18N
## Compilar
* rellenar el fichero i18n con los textos en distintos idiomas
* compilarlo, usando i18n_compiler.py
* generará el fichero i18n.py

## Uso
```
internationatization = i18n()
print internationatization["session_info_login"]["es"]
En Flask:
idioma_html = request.headers.get('Accept-Language')
print internationatization["session_info_login"][idioma_html]
```

## Diseño del fichero i18n
```
[identificador de la cadena]
codigo de idioma 1|Frase en el idioma del código 1
...
codigo de idioma N|Frase en el idioma del código N

Ejemplo:
[session_info_login]
en|You must log in to the application
es|Debes iniciar sesión en la aplicación
```
## Diseño del código
* Se utiliza un Singleton para evitar carga de las cadenas cada vez que se usa el sistema
* i18n_item.py guarda los diferentes idiomas y traduce 'Accept-Language' de HTML a código de idioma