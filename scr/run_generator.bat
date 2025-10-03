@echo off
chcp 65001 >nul
title Profile Manager - Генератор анкет
echo.
echo 👤 Запуск генератора анкет...
echo.
python src/profile_generator.py
pause