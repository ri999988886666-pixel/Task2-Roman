import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import markdown

class ProfileGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("👤 Генератор Анкет - Profile Manager")
        self.root.geometry("800x700")
        
        self.profiles_dir = "profiles"
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            
        self.setup_ui()
        
    def setup_ui(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            title_frame, 
            text="👤 Генератор Анкет", 
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(expand=True)
        
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка 1: Основная информация
        self.setup_personal_tab()
        
        # Вкладка 2: Навыки и образование
        self.setup_skills_tab()
        
        # Вкладка 3: Проекты и опыт
        self.setup_projects_tab()
        
        # Кнопки управления
        self.setup_controls()
    
    def setup_personal_tab(self):
        """Вкладка личной информации"""
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="👤 Личная информация")
        
        fields = [
            ("ФИО:", "full_name"),
            ("Должность:", "position"),
            ("Email:", "email"),
            ("Телефон:", "phone"),
            ("Город:", "city"),
            ("GitHub:", "github"),
            ("Telegram:", "telegram")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(fields):
            frame = tk.Frame(tab1)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=label, width=12, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = entry
        
        # О себе
        about_frame = tk.Frame(tab1)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(about_frame, text="О себе:", anchor='w').pack(fill=tk.X)
        self.about_text = scrolledtext.ScrolledText(about_frame, height=8)
        self.about_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def setup_skills_tab(self):
        """Вкладка навыков"""
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="🛠️ Навыки")
        
        # Языки программирования
        prog_frame = tk.Frame(tab2)
        prog_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(prog_frame, text="Языки программирования:", anchor='w').pack(fill=tk.X)
        self.prog_langs_text = scrolledtext.ScrolledText(prog_frame, height=4)
        self.prog_langs_text.pack(fill=tk.X, pady=(5, 0))
        
        # Фреймворки
        frameworks_frame = tk.Frame(tab2)
        frameworks_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frameworks_frame, text="Фреймворки и библиотеки:", anchor='w').pack(fill=tk.X)
        self.frameworks_text = scrolledtext.ScrolledText(frameworks_frame, height=4)
        self.frameworks_text.pack(fill=tk.X, pady=(5, 0))
        
        # Инструменты
        tools_frame = tk.Frame(tab2)
        tools_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(tools_frame, text="Инструменты:", anchor='w').pack(fill=tk.X)
        self.tools_text = scrolledtext.ScrolledText(tools_frame, height=3)
        self.tools_text.pack(fill=tk.X, pady=(5, 0))
        
        # Образование
        education_frame = tk.Frame(tab2)
        education_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(education_frame, text="Образование:", anchor='w').pack(fill=tk.X)
        self.education_text = scrolledtext.ScrolledText(education_frame, height=4)
        self.education_text.pack(fill=tk.X, pady=(5, 0))
    
    def setup_projects_tab(self):
        """Вкладка проектов"""
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="💼 Проекты")
        
        # Опыт работы
        experience_frame = tk.Frame(tab3)
        experience_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(experience_frame, text="Опыт работы:", anchor='w').pack(fill=tk.X)
        self.experience_text = scrolledtext.ScrolledText(experience_frame, height=6)
        self.experience_text.pack(fill=tk.X, pady=(5, 0))
        
        # Проекты
        projects_frame = tk.Frame(tab3)
        projects_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(projects_frame, text="Проекты:", anchor='w').pack(fill=tk.X)
        self.projects_text = scrolledtext.ScrolledText(projects_frame, height=6)
        self.projects_text.pack(fill=tk.X, pady=(5, 0))
        
        # Достижения
        achievements_frame = tk.Frame(tab3)
        achievements_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(achievements_frame, text="Достижения:", anchor='w').pack(fill=tk.X)
        self.achievements_text = scrolledtext.ScrolledText(achievements_frame, height=4)
        self.achievements_text.pack(fill=tk.X, pady=(5, 0))
    
    def setup_controls(self):
        """Кнопки управления"""
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(
            controls_frame, 
            text="🔄 Очистить все", 
            command=self.clear_all
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            controls_frame, 
            text="👁 Предпросмотр", 
            command=self.preview_profile
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            controls_frame, 
            text="💾 Сохранить анкету", 
            command=self.save_profile,
            bg='#27ae60',
            fg='white'
        ).pack(side=tk.LEFT)
    
    def clear_all(self):
        """Очистить все поля"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        self.about_text.delete('1.0', tk.END)
        self.prog_langs_text.delete('1.0', tk.END)
        self.frameworks_text.delete('1.0', tk.END)
        self.tools_text.delete('1.0', tk.END)
        self.education_text.delete('1.0', tk.END)
        self.experience_text.delete('1.0', tk.END)
        self.projects_text.delete('1.0', tk.END)
        self.achievements_text.delete('1.0', tk.END)
    
    def generate_profile_data(self):
        """Генерация данных анкеты"""
        return {
            "personal": {
                "full_name": self.entries['full_name'].get(),
                "position": self.entries['position'].get(),
                "email": self.entries['email'].get(),
                "phone": self.entries['phone'].get(),
                "city": self.entries['city'].get(),
                "github": self.entries['github'].get(),
                "telegram": self.entries['telegram'].get(),
                "about": self.about_text.get('1.0', tk.END).strip()
            },
            "skills": {
                "programming_languages": self.prog_langs_text.get('1.0', tk.END).strip(),
                "frameworks": self.frameworks_text.get('1.0', tk.END).strip(),
                "tools": self.tools_text.get('1.0', tk.END).strip(),
                "education": self.education_text.get('1.0', tk.END).strip()
            },
            "projects": {
                "experience": self.experience_text.get('1.0', tk.END).strip(),
                "projects": self.projects_text.get('1.0', tk.END).strip(),
                "achievements": self.achievements_text.get('1.0', tk.END).strip()
            },
            "meta": {
                "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "version": "1.0"
            }
        }
    
    def generate_markdown(self, profile_data):
        """Генерация Markdown из данных"""
        personal = profile_data['personal']
        skills = profile_data['skills']
        projects = profile_data['projects']
        
        markdown_content = f"""# 👋 Привет! Я {personal['full_name'] or 'Имя Фамилия'}

## 🚀 {personal['position'] or 'Должность'}
📍 {personal['city'] or 'Город'}

{personal['about'] or '*Расскажите о себе*'}

## 📫 Контакты:
- 📧 **Email:** {personal['email'] or 'email@example.com'}
- 📱 **Телефон:** {personal['phone'] or '+7 XXX XXX-XX-XX'}
- 💼 **GitHub:** [{personal['github'] or 'username'}](https://github.com/{personal['github'] or 'username'})
- 📢 **Telegram:** {personal['telegram'] or '@username'}

## 🛠️ Навыки:

### Языки программирования:
{self.format_text(skills['programming_languages'])}

### Фреймворки и библиотеки:
{self.format_text(skills['frameworks'])}

### Инструменты:
{self.format_text(skills['tools'])}

## 🎓 Образование:
{self.format_text(skills['education'])}

## 💼 Опыт работы:
{self.format_text(projects['experience'])}

## 🎯 Проекты:
{self.format_text(projects['projects'])}

## 🏆 Достижения:
{self.format_text(projects['achievements'])}

---

*Анкета создана {datetime.now().strftime('%d.%m.%Y')} с помощью Profile Manager*"""
        
        return markdown_content
    
    def format_text(self, text, prefix="- "):
        """Форматирование текста в список"""
        if not text.strip():
            return f"{prefix}Не указано"
        
        lines = text.strip().split('\n')
        formatted_lines = [f"{prefix}{line.strip()}" for line in lines if line.strip()]
        return '\n'.join(formatted_lines)
    
    def preview_profile(self):
        """Предпросмотр анкеты"""
        profile_data = self.generate_profile_data()
        markdown_content = self.generate_markdown(profile_data)
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Предпросмотр анкеты")
        preview_window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, font=('Courier New', 10))
        text_widget.insert(tk.END, markdown_content)
        
        scrollbar = tk.Scrollbar(preview_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def save_profile(self):
        """Сохранение анкеты"""
        if not self.entries['full_name'].get():
            messagebox.showerror("Ошибка", "Введите ФИО!")
            return
        
        profile_data = self.generate_profile_data()
        markdown_content = self.generate_markdown(profile_data)
        
        # Создаем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_{self.entries['full_name'].get().replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(self.profiles_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Также сохраняем JSON для быстрого чтения
            json_filename = f"profile_{self.entries['full_name'].get().replace(' ', '_')}_{timestamp}.json"
            json_filepath = os.path.join(self.profiles_dir, json_filename)
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Успех", f"Анкета сохранена!\n\nMarkdown: {filename}\nJSON: {json_filename}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

def main():
    root = tk.Tk()
    app = ProfileGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()