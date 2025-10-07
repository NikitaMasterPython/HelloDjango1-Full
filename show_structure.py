import os


def print_structure(startpath, max_level=3):
    """Печатает структуру проекта"""
    print("СТРУКТУРА ПРОЕКТА:")
    print("=" * 60)

    for root, dirs, files in os.walk(startpath):
        # Пропускаем служебные папки
        if any(skip in root for skip in ['__pycache__', '.git', '.idea', 'venv', 'env']):
            continue

        level = root.replace(startpath, '').count(os.sep)
        if level > max_level:
            continue

        indent = '    ' * level
        print(f"{indent}📁 {os.path.basename(root)}/")

        # Показываем только важные файлы
        subindent = '    ' * (level + 1)
        for file in files:
            if file.endswith(('.py', '.html', '.txt', '.md', 'Dockerfile', 'requirements.txt')):
                print(f"{subindent}📄 {file}")


if __name__ == "__main__":
    print_structure('.')

    # Проверяем ключевые файлы Django
    print("\n" + "=" * 60)
    print("ПРОВЕРКА КЛЮЧЕВЫХ ФАЙЛОВ:")

    key_files = {
        'manage.py': 'Основной файл Django',
        'requirements.txt': 'Зависимости Python',
        'Dockerfile': 'Конфигурация Docker',
        '.gitignore': 'Исключения для Git',
    }

    for file, description in key_files.items():
        exists = "✅ ЕСТЬ" if os.path.exists(file) else "❌ ОТСУТСТВУЕТ"
        print(f"{exists} {file} - {description}")