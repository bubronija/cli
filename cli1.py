import argparse
import os
import re
import sys

def main():
    parser = argparse.ArgumentParser(
        description = "CLI-прототип"
    )

    parser.add_argument("--package", required=True, help="имя пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес репозитория")
    parser.add_argument("--mode", choices=["local", "remote", "test"], required=True, help="расположение репозитория (local, remote, test).")
    parser.add_argument("--version", required=True, help="версия пакета")
    parser.add_argument("--max-depth", type=int, required=True, help="глубина")
    parser.add_argument("--filter", required=True, help="фильтрация пакетов")
    args = parser.parse_args()
    errors = []

    if not re.match(r"^[a-zA-Z0-9_\-]+$", args.package):
        errors.append("Ошибка. Недопустимое имя пакета")

    if args.mode == "remote" and not re.match(r"^https?://", args.repo):
        errors.append("Ошибка Для режима remote требуется URL-адрес репозитория.")

    if args.mode == "local" and not os.path.exists(args.repo):
        errors.append("Ошибка. Для режима local требуется существующий путь к файлу или каталогу.")

    if args.mode == "test" and not args.repo.endswith(".zip"):
        errors.append("Ошибка. Для режима test требуется путь к zip-файлу тестового репозитория.")

    if not re.match(r"^[0-9a-zA-Z.\-_]+$", args.version):
        errors.append("Ошибка. Недопустимый формат версии пакета.")

    if args.max_depth <= 0:
        errors.append("Ошибка. Глубина должна быть положительным числом")

    if not args.filter.strip():
        errors.append("Ошибка. Подстрока для фильтрации не может быть пустой.")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    config = vars(args)
    for key, value in config.items():
        print(f"{key} = {value}")


if __name__ == "__main__":
    main()
#python cli1.py --package mypkg --repo https://github.com/users/bubronija/projects/1.git --mode remote --version 1.0.0 --max-depth 3 --filter util