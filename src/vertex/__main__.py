# __main__.py
from pathlib import Path
import os

from PyInstaller.__main__ import run as pyinstaller_run

from .minicli import CLI
from .templates import TEMPLATES


def main():
    cli = CLI()

    # ------------------
    # build command
    # ------------------
    @cli.command("build")
    def build_executable(
        script_path: str,
        onefile: bool = False,
        windowed: bool = False,
    ):
        """
        Build an executable from a Python script using PyInstaller.
        """
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        args = ["--clean"]

        if onefile:
            args.append("--onefile")
        if windowed:
            args.append("--windowed")

        args.append(script_path)

        print(f"Running PyInstaller with args: {args}")
        pyinstaller_run(args)

    # ------------------
    # init command
    # ------------------
    @cli.command("init")
    def init(kind: str = "game"):
        """Initialize a project template"""
        if kind not in TEMPLATES:
            print("Available templates:", ", ".join(TEMPLATES))
            return

        for rel_path, content in TEMPLATES[kind].items():
            path = Path.cwd() / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)

            if path.exists():
                print(f"Skipped existing file: {rel_path}")
                continue

            path.write_text(content, encoding="utf-8")
            print(f"Created {rel_path}")

        print(f"Template '{kind}' initialized ✔")

    cli.run()


if __name__ == "__main__":
    main()
