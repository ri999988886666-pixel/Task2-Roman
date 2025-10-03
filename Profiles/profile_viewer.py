import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import glob
from datetime import datetime

class ProfileViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Просмотр анкет - Profile Manager")
        self.root.geometry("900x600")
        
        self.profiles_dir = "profiles"
        self.setup_ui()
        self.load_profiles()
    
    def setup_ui(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            title_frame, 
            text="🔍 Просмотр анкет", 
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(expand=True)
        
        # Поиск и фильтры
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="Поиск по имени:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        tk.Label(search_frame, text="Тип файла:").pack(side=tk.LEFT, padx=(20, 0))
        self.file_type_var = tk.StringVar(value="Все")
        file_type_combo = ttk.Combobox(search_frame, textvariable=self.file_type_var, 
                                     values=["Все", "Markdown", "JSON"])
        file_type_combo.pack(side=tk.LEFT, padx=5)
        file_type_combo.bind('<<ComboboxSelected>>', self.on_search)
        
        tk.Button(search_frame, text="🔄 Обновить", command=self.load_profiles).pack(side=tk.RIGHT)
        
        # Основной контейнер
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Список анкет
        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(left_frame, text="Список анкет:", font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.tree = ttk.Treeview(left_frame, columns=('Имя', 'Должность', 'Дата'), show='headings', height=15)
        self.tree.heading('Имя', text='Имя')
        self.tree.heading('Должность', text='Должность')
        self.tree.heading('Дата', text='Дата создания')
        
        self.tree.column('Имя', width=150)
        self.tree.column('Должность', width=120)
        self.tree.column('Дата', width=120)
        
        scrollbar_tree = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind('<<TreeviewSelect>>', self.on_profile_select)
        
        # Детали анкеты
        right_frame = tk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Вкладки для разных форматов просмотра
        self.view_notebook = ttk.Notebook(right_frame)
        self.view_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка Markdown
        md_frame = ttk.Frame(self.view_notebook)
        self.view_notebook.add(md_frame, text="Markdown")
        
        self.md_text = scrolledtext.ScrolledText(md_frame, wrap=tk.WORD, font=('Courier New', 9))
        self.md_text.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка JSON
        json_frame = ttk.Frame(self.view_notebook)
        self.view_notebook.add(json_frame, text="JSON")
        
        self.json_text = scrolledtext.ScrolledText(json_frame, wrap=tk.WORD, font=('Courier New', 9))
        self.json_text.pack(fill=tk.BOTH, expand=True)
        
        # Статистика
        self.stats_label = tk.Label(self.root, text="Загрузка...", font=('Arial', 9))
        self.stats_label.pack(fill=tk.X, padx=20, pady=5)
    
    def load_profiles(self):
        """Загрузка списка анкет"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not os.path.exists(self.profiles_dir):
            self.stats_label.config(text="Папка с анкетами не найдена")
            return
        
        search_term = self.search_var.get().lower()
        file_type_filter = self.file_type_var.get()
        
        # Ищем файлы
        all_files = []
        if file_type_filter in ["Все", "Markdown"]:
            all_files.extend(glob.glob(os.path.join(self.profiles_dir, "*.md")))
        if file_type_filter in ["Все", "JSON"]:
            all_files.extend(glob.glob(os.path.join(self.profiles_dir, "*.json")))
        
        valid_profiles = 0
        
        for filepath in all_files:
            try:
                filename = os.path.basename(filepath)
                
                # Фильтрация по поиску
                if search_term and search_term not in filename.lower():
                    continue
                
                # Получаем информацию об анкете
                profile_info = self.get_profile_info(filepath)
                if profile_info:
                    self.tree.insert('', 'end', 
                                   values=(profile_info['name'], 
                                         profile_info['position'],
                                         profile_info['date']),
                                   tags=(filepath, profile_info['type']))
                    
                    valid_profiles += 1
                
            except Exception as e:
                print(f"Ошибка загрузки файла {filepath}: {e}")
        
        self.stats_label.config(text=f"Найдено анкет: {valid_profiles}")
    
    def get_profile_info(self, filepath):
        """Получить информацию об анкете"""
        filename = os.path.basename(filepath)
        file_ext = os.path.splitext(filename)[1]
        
        try:
            if file_ext == '.json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                return {
                    'name': data['personal']['full_name'],
                    'position': data['personal']['position'],
                    'date': data['meta']['created'],
                    'type': 'JSON'
                }
            
            elif file_ext == '.md':
                # Для MD файлов парсим первую строку для имени
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                
                # Извлекаем имя из формата "# 👋 Привет! Я Имя Фамилия"
                name = first_line.replace('# 👋 Привет! Я ', '').strip()
                
                stats = os.stat(filepath)
                date_str = datetime.fromtimestamp(stats.st_ctime).strftime('%d.%m.%Y %H:%M')
                
                return {
                    'name': name,
                    'position': 'Не указано',
                    'date': date_str,
                    'type': 'Markdown'
                }
        
        except Exception as e:
            print(f"Ошибка чтения файла {filepath}: {e}")
            return None
    
    def on_search(self, event=None):
        """Обработка поиска"""
        self.load_profiles()
    
    def on_profile_select(self, event):
        """Обработка выбора анкеты"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        filepath = self.tree.item(item, 'tags')[0]
        file_type = self.tree.item(item, 'tags')[1]
        
        try:
            if file_type == 'JSON':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.json_text.delete('1.0', tk.END)
                self.json_text.insert('1.0', json.dumps(data, indent=2, ensure_ascii=False))
                
                # Генерируем Markdown из JSON
                markdown_content = self.json_to_markdown(data)
                self.md_text.delete('1.0', tk.END)
                self.md_text.insert('1.0', markdown_content)
                
            else:  # Markdown
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.md_text.delete('1.0', tk.END)
                self.md_text.insert('1.0', content)
                
                # Пытаемся найти соответствующий JSON файл
                json_filepath = filepath.replace('.md', '.json')
                if os.path.exists(json_filepath):
                    with open(json_filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.json_text.delete('1.0', tk.END)
                    self.json_text.insert('1.0', json.dumps(data, indent=2, ensure_ascii=False))
                else:
                    self.json_text.delete('1.0', tk.END)
                    self.json_text.insert('1.0', "JSON файл не найден")
            
        except Exception as e:
            self.md_text.delete('1.0', tk.END)
            self.md_text.insert('1.0', f"Ошибка загрузки: {str(e)}")
            self.json_text.delete('1.0', tk.END)
            self.json_text.insert('1.0', f"Ошибка загрузки: {str(e)}")
    
    def json_to_markdown(self, data):
        """Конвертация JSON в Markdown"""
        personal = data['personal']
        skills = data['skills']
        projects = data['projects']
        
        markdown_content = f"""# 👋 Привет! Я {personal['full_name']}

## 🚀 {personal['position']}
📍 {personal['city']}

{personal['about']}

## 📫 Контакты:
- 📧 **Email:** {personal['email']}
- 📱 **Телефон:** {personal['phone']}
- 💼 **GitHub:** [{personal['github']}](https://github.com/{personal['github']})
- 📢 **Telegram:** {personal['telegram']}

## 🛠️ Навыки:

### Языки программирования:
{self.format_text_for_display(skills['programming_languages'])}

### Фреймворки и библиотеки:
{self.format_text_for_display(skills['frameworks'])}

### Инструменты:
{self.format_text_for_display(skills['tools'])}

## 🎓 Образование:
{self.format_text_for_display(skills['education'])}

## 💼 Опыт работы:
{self.format_text_for_display(projects['experience'])}

## 🎯 Проекты:
{self.format_text_for_display(projects['projects'])}

## 🏆 Достижения:
{self.format_text_for_display(projects['achievements'])}"""
        
        return markdown_content
    
    def format_text_for_display(self, text):
        """Форматирование текста для отображения"""
        if not text.strip() or text.strip() == "- Не указано":
            return "- Не указано"
        
        lines = text.strip().split('\n')
        return '\n'.join(lines)

def main():
    root = tk.Tk()
    app = ProfileViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()