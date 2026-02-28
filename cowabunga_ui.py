import flet as ft
import os
import threading
from cowabunga_core import KEYS, process_file


def run_ui():
    def main(page: ft.Page):
        page.title = "Cowabunga Decryptor"
        page.theme_mode = ft.ThemeMode.DARK
        page.window.width = 600
        page.window.height = 500
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 30

        input_file = ft.Ref[ft.TextField]()
        output_file = ft.Ref[ft.TextField]()
        key_dropdown = ft.Ref[ft.Dropdown]()
        custom_key = ft.Ref[ft.TextField]()
        progress_bar = ft.Ref[ft.ProgressBar]()
        status_text = ft.Ref[ft.Text]()
        decrypt_button = ft.Ref[ft.ElevatedButton]()

        def pick_input_file(e):
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            file_path = filedialog.askopenfilename(
                title="Select input .pie file",
                filetypes=[("PIE files", "*.pie"), ("All files", "*.*")]
            )
            root.destroy()
            if file_path:
                input_file.current.value = file_path
                name, ext = os.path.splitext(file_path)
                output_file.current.value = name + ".zip"
                page.update()

        def start_decryption(e):
            if not input_file.current.value or not output_file.current.value:
                status_text.current.value = "Please select both input and output files."
                status_text.current.color = ft.Colors.RED_400
                page.update()
                return

            game_key = None
            if custom_key.current.value:
                try:
                    game_key = int(custom_key.current.value.replace("0x", ""), 16)
                except ValueError:
                    status_text.current.value = "Invalid custom key format."
                    status_text.current.color = ft.Colors.RED_400
                    page.update()
                    return
            else:
                game_key = KEYS[key_dropdown.current.value]

            decrypt_button.current.disabled = True
            progress_bar.current.value = 0
            status_text.current.value = "Processing..."
            status_text.current.color = ft.Colors.BLUE_400
            page.update()

            def work():
                try:
                    success, error = process_file(
                        input_file.current.value,
                        output_file.current.value,
                        game_key,
                        progress_callback=lambda p: update_progress(p)
                    )
                    if success:
                        status_text.current.value = "Success! File decrypted."
                        status_text.current.color = ft.Colors.GREEN_400
                    else:
                        status_text.current.value = f"Error: {error}"
                        status_text.current.color = ft.Colors.RED_400
                except Exception as ex:
                    status_text.current.value = f"Exception: {str(ex)}"
                    status_text.current.color = ft.Colors.RED_400
                finally:
                    decrypt_button.current.disabled = False
                    page.update()

            def update_progress(p):
                progress_bar.current.value = p
                page.update()

            threading.Thread(target=work, daemon=True).start()

        page.add(
            ft.Text("Cowabunga Decryptor", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Digital Eclipse Assets Decryption Tool", size=16, italic=True, color=ft.Colors.GREY_400),
            ft.Divider(height=20),
            ft.Row([
                ft.TextField(ref=input_file, label="Input .pie File", expand=True, read_only=True),
                ft.IconButton(icon=ft.Icons.FOLDER_OPEN, on_click=pick_input_file)
            ]),
            ft.TextField(ref=output_file, label="Output File"),
            ft.Row([
                ft.Dropdown(
                    ref=key_dropdown,
                    label="Game Key",
                    value="cowabunga",
                    options=[ft.dropdown.Option(k) for k in KEYS.keys()],
                    expand=True
                ),
                ft.TextField(ref=custom_key, label="Custom Hex Key", width=150)
            ]),
            ft.Container(height=10),
            ft.ElevatedButton(
                ref=decrypt_button,
                content=ft.Text("Decrypt Now"),
                icon=ft.Icons.LOCK_OPEN,
                on_click=start_decryption,
                style=ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_700,
                    padding=20
                )
            ),
            ft.ProgressBar(ref=progress_bar, value=0, height=10, border_radius=5),
            ft.Text(ref=status_text, value="", size=14)
        )

    ft.app(target=main)

if __name__ == "__main__":
    run_ui()
