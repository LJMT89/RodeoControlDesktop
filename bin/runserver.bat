@echo off

REM Activar el entorno virtual
call "D:\IDEAFIX\RodeoControl\virtualenv\windows\rodeo_venv\Scripts\activate"

REM Ir al directorio del proyecto
cd "D:\IDEAFIX\RodeoControl\Repositorio\Web\RodeoControl\rodeo_control"

REM Lanzar el servidor Django
python manage.py runserver 0.0.0.0:8000
