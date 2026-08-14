@echo off
echo ========================================
echo  DaeZone Order Status Automation
echo ========================================
echo.
echo This runs the background task that:
echo - Updates Pending to Processing (30 sec)
echo - Updates Shipped to Delivered (on date)
echo.
echo Keep this window open for automation
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

python manage.py run_scheduler
