import argparse
import os
import re
import sys
import urllib.request

def get_cargo_dependencies(repo_url, version):
    cargo_data = None

    if repo_url.startswith("http"):
        repo_url = repo_url.replace(".git", "")
        branches = ["main", "master", "stable", "trunk", "dev"]

        for branch in branches:
            cargo_url = repo_url.replace("github.com", "raw.githubusercontent.com") + f"/{branch}/Cargo.toml"
            try:
                with urllib.request.urlopen(cargo_url) as response:
                    cargo_data = response.read().decode("utf-8")
                    break
            except Exception:
                continue
    else:
        cargo_path = os.path.join(repo_url, "Cargo.toml")
        if os.path.exists(cargo_path):
            with open(cargo_path, "r", encoding="utf-8") as f:
                cargo_data = f.read()

    if cargo_data is None:
        print("Ошибка, не удалось найти или загрузить Cargo.toml")
        return []

    dependencies = []
    in_deps = False
    for line in cargo_data.splitlines():
        line = line.strip()
        if line.startswith("[dependencies]"):
            in_deps = True
            continue
        if in_deps:
            if line.startswith("[") and not line.startswith("[dependencies]"):
                break
            if line and not line.startswith("#"):
                dep_name = line.split("=")[0].strip()
                dependencies.append(dep_name)

    return dependencies


def main():
    parser = argparse.ArgumentParser(
        description="CLI-прототип. Сбор данных зависимостей"
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
        errors.append("Ошибка. Для режима remote требуется URL-адрес репозитория.")

    if args.mode == "local" and not os.path.exists(args.repo):
        errors.append("Ошибка. Для режима local требуется существующий путь к файлу или каталогу.")

    if args.mode == "test" and not args.repo.endswith(".zip"):
        errors.append("Ошибка. Для режима test требуется путь к zip-файлу тестового репозитория.")

    if not re.match(r"^[0-9a-zA-Z.\-_]+$", args.version):
        errors.append("Ошибка. Недопустимый формат версии пакета.")

    if args.max_depth <= 0:
        errors.append("Ошибка. Глубина должна быть положительным числом.")

    if not args.filter.strip():
        errors.append("Ошибка. Подстрока для фильтрации не может быть пустой.")
    if errors:

        for e in errors:
            print(e)
        sys.exit(1)

    print(f"Анализ пакета: {args.package} (версия {args.version})")
    print(f"Режим: {args.mode}")
    print(f"Репозиторий: {args.repo}")
    print("\nПрямые зависимости")

    deps = get_cargo_dependencies(args.repo, args.version)
    if deps:
        for d in deps:
            print(f"- {d}")
    else:
        print("не удалось извлечь зависимости, не существуют.")


if __name__ == "__main__":
    main()
#python cli1.py --package mypkg --repo https://github.com/rust-lang/rustfmt --mode remote --version 1.0.0 --max-depth 3 --filter aaa
#python cli1.py --package cargo --repo https://github.com/rust-lang/cargo --mode remote --version 1.0.0 --max-depth 1 --filter bbb
#python cli1.py --package testpkg --repo https://github.com/rust-lang/rust.git --mode remote --version 1.0.0 --max-depth 1 --filter abc
#нет зависимостей