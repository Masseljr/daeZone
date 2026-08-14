@echo off
echo ========================================
echo   DaeZone - Load Sample Data
echo ========================================
echo.
echo This will create sample categories and products
echo for testing the e-commerce site.
echo.

python manage.py load_sample_data

echo.
echo ========================================
echo.
pause
