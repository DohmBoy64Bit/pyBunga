# 🐢 Pybunga Decryptor (Python Port)

<p align="center">
  <img src="img/ProgramImage.png" alt="Pybunga UI">
</p>

A modern, cross-platform port of the Cowabunga decryption tool for Digital Eclipse assets. This version features a modular Python architecture with both a command-line interface (CLI) and a Material Design graphical user interface (GUI).

## ✨ Features

- **Material Design GUI**: Clean, modern interface built with [Flet](https://flet.dev/).
- **Efficient CLI**: Fast, terminal-based processing for power users.
- **Ported Logic**: Exact replication of the original Rust decryption algorithm.
- **Built-in Keys**: Pre-configured keys for a wide range of Digital Eclipse collections (Atari, Blizzard, Yu-Gi-Oh!, TMNT, etc.).
- **Progress Tracking**: Real-time feedback for large file decryptions.
- **ZIP Validation**: Automatically verifies if the output is a valid ZIP file.

## 🎮 Supported Games

The following games are supported with pre-defined keys:

- **Teenage Mutant Ninja Turtles: The Cowabunga Collection** (`cowabunga`)
- **Atari 50: The Anniversary Celebration** (+ DLCs) (`atari`, `atari-dlc1`, `atari-dlc2`, `atari-dlc3`)
- **The Making of Karateka** (`making-karateka`)
- **Garbage Pail Kids: Mad Mike and the Quest for Stale Gum** (`garbage-pail-kids`)
- **Llamasoft: The Jeff Minter Story** (`jeff-minter`)
- **Tetris Forever** (same key as `jeff-minter`)
- **Blizzard Arcade Collection** (specifically `music.pie`) (`blizzard-arcade`)
- **Mighty Morphin Power Rangers: Rita's Rewind** (`mighty-morphin`)
- **Yu-Gi-Oh! EARLY DAYS COLLECTION** (`yu-gi-oh`)
- **Mortal Kombat Legacy Collection** (`mortal-kombat-lc`)
- **Golden Tee Arcade Classics** (`golden-tee`)
- **Rayman: 30th Anniversary Edition** (`rayman30th`)

### 🔑 List of Possible Keys

- `cowabunga`
- `atari`
- `atari-dlc1`
- `atari-dlc2`
- `atari-dlc3`
- `making-karateka`
- `garbage-pail-kids`
- `jeff-minter`
- `blizzard-arcade`
- `mighty-morphin`
- `yu-gi-oh`
- `mortal-kombat-lc`
- `golden-tee`
- `rayman30th`

## 🚀 Download

You can download the pre-compiled, single-file Windows executables directly from the GitHub releases page:
- 🖥️ **GUI Version:** [Download Pybunga.exe v1.0.0 (95MB)](https://github.com/DohmBoy64Bit/pyBunga/releases/latest/download/Pybunga.exe)
- ⚙️ **CLI Version:** [Download Pybunga-CLI.exe v1.0.0 (8MB)](https://github.com/DohmBoy64Bit/pyBunga/releases/latest/download/Pybunga-CLI.exe)

No installation or Python environment required!

### 🖥️ Enabling Console Output (For .exe)
If you want to see real-time decryption progress logs while using the GUI:
1. Right-click `Pybunga.exe` and select **Create shortcut**.
2. Right-click the new shortcut and select **Properties**.
3. In the **Target** field, add a space and then `-console` at the very end.
   *(Example: `...\Pybunga.exe" -console`)*
4. Use this shortcut to launch the app!

## 🚀 Quick Start (From Source)

### 1. Prerequisites
- Python 3.9 or higher.

### 2. Setup
Clone the repository and navigate to the Python version folder:
```bash
cd cowabunga_python
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install flet
```

### 3. Running

#### Launch the GUI
Simply run the entry point without arguments:
```bash
python main.py
```

#### Use the CLI (Interactive Menu)
To bypass the GUI and run the interactive console wizard:
```bash
python main.py --cli
```

## 🛠️ CLI Usage

The Pybunga CLI (`Pybunga-CLI.exe` or `python main.py --cli`) now features a fully interactive wizard!

Simply launch the CLI and it will prompt you step-by-step for the required information:
1. Select the game key from a numbered list (or choose `0` to enter a custom hex key).
2. Provide the path to the input `.pie` file.
3. Provide the path for the output file.

Sit back and watch the decryption progress in the console!

## 📂 Project Structure

- `main.py`: Dual-mode entry point (GUI/CLI).
- `cowabunga_ui.py`: Material Design interface code.
- `cowabunga_cli.py`: Command-line interface logic.
- `cowabunga_core.py`: Core decryption algorithm & file processing.

## 👏 Credits

- **Original Tool**: [Cowabunga](https://github.com/Masquerade64/Cowabunga/tree/main) by [Masquerade64](https://github.com/Masquerade64/).
- **Ported by**: DohmBoy64bit
- **Original Tool**: [Cowabunga](https://github.com/Masquerade64/Cowabunga/tree/main) by [Masquerade64](https://github.com/Masquerade64/).
- **Ported by**: DohmBoy64bit


## 📄 License

This project is licensed under the [MIT License](LICENSE).
