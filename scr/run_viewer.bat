@echo off
chcp 65001 >nul
title Profile Manager - Просмотр анкет
echo.
echo 🔍 Запуск просмотрщика анкет...
echo.
python src/profile_viewer.py
pause