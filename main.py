import sys
from cowabunga_cli import run_cli
from cowabunga_ui import run_ui

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_ui()

if __name__ == "__main__":
    main()
