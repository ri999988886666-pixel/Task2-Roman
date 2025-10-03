#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🚀 Меню запуска Profile Manager
"""

import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print("🚀 Profile Manager")
    print("=" * 40)
    print("1. 👤 Генератор анкет")
    print("2. 🔍 Просмотр анкет")
    print("3. 📊 Статистика")
    print("4. 🚪 Выход")
    print("=" * 40)

def show_statistics():
    clear_screen()
    print("📊 Статистика анкет")
    print("=" * 40)
    
    profiles_dir = "profiles"
    if not os.path.exists(profiles_dir):
        print("Папка с анкетами не найдена")
        return
    
    md_files = [f for f in os.listdir(profiles_dir) if f.endswith('.md')]
    json_files = [f for f in os.listdir(profiles_dir) if f.endswith('.json')]
    
    print(f"📁 Всего анкет: {len(md_files)}")
    print(f"📊 Файлов JSON: {len(json_files)}")
    
    if md_files:
        print("\n📋 Последние анкеты:")
        for i, profile_file in enumerate(md_files[-5:], 1):
            print(f"  {i}. {profile_file}")

def main():
    while True:
        show_menu()
        choice = input("Выберите действие [1-4]: ").strip()
        
        if choice == '1':
            print("\nЗапуск генератора анкет...")
            try:
                subprocess.run([sys.executable, "src/profile_generator.py"])
            except Exception as e:
                print(f"Ошибка запуска: {e}")
                input("Нажмите Enter для продолжения...")
                
        elif choice == '2':
            print("\nЗапуск просмотрщика анкет...")
            try:
                subprocess.run([sys.executable, "src/profile_viewer.py"])
            except Exception as e:
                print(f"Ошибка запуска: {e}")
                input("Нажмите Enter для продолжения...")
                
        elif choice == '3':
            show_statistics()
            input("Нажмите Enter для продолжения...")
            
        elif choice == '4':
            print("\nДо свидания! 👋")
            break
            
        else:
            print("❌ Неверный выбор!")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()