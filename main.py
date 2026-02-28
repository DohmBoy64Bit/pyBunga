import sys
import os
from cowabunga_cli import run_cli
from cowabunga_ui import run_ui

def main():
    if "-console" in sys.argv:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.AllocConsole()
            sys.stdout = open("CONOUT$", "w")
            sys.stderr = open("CONOUT$", "w")
            print("Pybunga Console Output Enabled.")
        sys.argv.remove("-console")

    import argparse
    parser = argparse.ArgumentParser(description="Pybunga Decryptor")
    parser.add_argument("--cli", action="store_true", help="Launch the interactive CLI wizard")
    args, unknown = parser.parse_known_args()

    if args.cli:
        run_cli()
    else:
        run_ui()

if __name__ == "__main__":
    main()
