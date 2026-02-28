import sys
import argparse
from cowabunga_core import KEYS, process_file

def run_cli():
    parser = argparse.ArgumentParser(
        description="Cowabunga: Decryption tool for Digital Eclipse assets.pie files (Python Version).",
        epilog="Example usage:\n  python main.py -k cowabunga assets.pie assets.zip\n  python main.py -c 0xFA5E893B assets.pie assets.zip"
    )
    
    parser.add_argument("input", help="Path to the input .pie file")
    parser.add_argument("output", help="Path to the output file")
    parser.add_argument("-k", "--key", choices=KEYS.keys(), default="cowabunga", help="Game key for decryption")
    parser.add_argument("-c", "--custom", help="Custom key in hexadecimal (e.g., 0xC90CA066)")

    args = parser.parse_args()

    if args.custom:
        try:
            game_key = int(args.custom.replace("0x", ""), 16)
        except ValueError:
            print(f"Error: Invalid custom key '{args.custom}'.")
            sys.exit(1)
    else:
        game_key = KEYS[args.key]

    print(f"Decrypting {args.input} -> {args.output}...")
    
    success, error = process_file(args.input, args.output, game_key, 
                                  progress_callback=lambda p: print(f"Progress: {p:.1%}", end='\r'))
    print()

    if success:
        print("Done!")
    else:
        print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
