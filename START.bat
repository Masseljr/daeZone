@echo off
echo ========================================
echo   DaeZone E-Commerce - Quick Start
echo ========================================
echo.

echo Checking if superuser exists...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"

if errorlevel 1 (
    echo.
    echo No admin user found. Creating one now...
    echo.
    echo Please enter admin credentials:
    python manage.py createsuperuser
) else (
    echo Admin user already exists!
)

echo.
echo ========================================
echo   Starting Django Development Server
echo ========================================
echo.
echo Access the site at: http://localhost:8000
echo Access admin panel: http://localhost:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
