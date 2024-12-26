import os

DEFAULT_COPYIGNORE_CONTENT = """# Список шаблонов для игнорирования файлов и папок
# Пример:
# *.log
# *.tmp
# папка_для_игнорирования
"""

def create_default_copyignore(ignore_file=".copyignore"):
    """Создает файл .copyignore с дефолтным содержимым, если его не существует."""
    if not os.path.exists(ignore_file):
        with open(ignore_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_COPYIGNORE_CONTENT)
        print(f"Создан файл {ignore_file} с дефолтным содержимым.")

def load_copyignore(ignore_file=".copyignore"):
    """Загружает список исключений из файла .copyignore."""
    ignore_patterns = []
    if os.path.exists(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as f:
            ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ignore_patterns

def is_ignored(path, ignore_patterns):
    """Проверяет, игнорируется ли файл или папка."""
    for pattern in ignore_patterns:
        if path.endswith(pattern) or pattern in path.split(os.sep):
            return True
    return False

def gather_files_content(root_dir, ignore_patterns, ignore_file=".copyignore", output_file="collected_files.txt"):
    """Рекурсивно собирает содержимое файлов, помечая их именами."""
    collected_content = []
    for root, dirs, files in os.walk(root_dir):
        # Исключаем директории
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            # Пропускаем файл .copyignore и файл, в который записывается результат
            if file_path.endswith(ignore_file) or file_path == output_file or is_ignored(file_path, ignore_patterns):
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                collected_content.append(f"===== {file_path} =====\n{file_content}\n")
            except (UnicodeDecodeError, OSError):
                # Пропускаем файлы, которые невозможно прочитать
                continue
    return "\n".join(collected_content)

def save_to_file(content, output_file="collected_files.txt"):
    """Сохраняет собранное содержимое в файл."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Собранное содержимое сохранено в файл: {output_file}")

def main():
    root_dir = os.getcwd()  # Текущая папка, откуда запускается скрипт
    ignore_file = os.path.join(root_dir, ".copyignore")
    
    # Создаем файл .copyignore, если он отсутствует
    create_default_copyignore(ignore_file)

    # Загружаем шаблоны для игнорирования
    ignore_patterns = load_copyignore(ignore_file)

    # Сбор содержимого файлов
    content = gather_files_content(root_dir, ignore_patterns, ignore_file)

    # Сохранение в файл
    output_file = os.path.join(root_dir, "collected_files.txt")
    save_to_file(content, output_file)

if __name__ == "__main__":
    main()
