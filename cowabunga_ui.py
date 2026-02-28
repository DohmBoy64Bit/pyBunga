import flet as ft
import os
import threading
import ctypes
from cowabunga_core import KEYS, process_file

def run_ui():
    # Set AppUserModelID on Windows so the taskbar icon updates correctly
    if os.name == 'nt':
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("pybunga.decryptor.ui.1.0")
        except Exception:
            pass

    async def main(page: ft.Page):
        page.title = "Pybunga Decryptor"
        page.theme_mode = ft.ThemeMode.DARK
        page.window.width = 620
        page.window.height = 610
        page.window.resizable = False
        page.window.icon = "img/icon.png"
        page.window.title_bar_hidden = True
        page.window.title_bar_buttons_hidden = True
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.padding = 0
        page.bgcolor = "#0D1117"

        input_file = ft.Ref[ft.TextField]()
        output_file = ft.Ref[ft.TextField]()
        key_dropdown = ft.Ref[ft.Dropdown]()
        custom_key = ft.Ref[ft.TextField]()
        progress_bar = ft.Ref[ft.ProgressBar]()
        status_text = ft.Ref[ft.Text]()
        decrypt_button = ft.Ref[ft.ElevatedButton]()

        async def close_app(e):
            await page.window.close()

        async def minimize_app(e):
            page.window.minimized = True
            page.update()

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
                name, _ = os.path.splitext(file_path)
                output_file.current.value = name + ".zip"
                page.update()

        def start_decryption(e):
            if not input_file.current.value or not output_file.current.value:
                status_text.current.value = "Please select both input and output files."
                status_text.current.color = "#FF6B6B"
                page.update()
                return

            game_key = None
            if custom_key.current.value:
                try:
                    game_key = int(custom_key.current.value.replace("0x", ""), 16)
                except ValueError:
                    status_text.current.value = "Invalid custom key format."
                    status_text.current.color = "#FF6B6B"
                    page.update()
                    return
            else:
                game_key = KEYS[key_dropdown.current.value]

            decrypt_button.current.disabled = True
            progress_bar.current.value = 0
            status_text.current.value = "Processing..."
            status_text.current.color = "#64B5F6"
            page.update()

            def work():
                try:
                    print(f"Starting decryption: {input_file.current.value}")
                    print(f"Output destination: {output_file.current.value}")
                    success, error = process_file(
                        input_file.current.value,
                        output_file.current.value,
                        game_key,
                        progress_callback=lambda p: update_progress(p)
                    )
                    if success:
                        print("\nDecryption completed successfully.")
                        status_text.current.value = "Success! File decrypted."
                        status_text.current.color = "#66BB6A"
                    else:
                        print(f"\nError during decryption: {error}")
                        status_text.current.value = f"Error: {error}"
                        status_text.current.color = "#FF6B6B"
                except Exception as ex:
                    print(f"\nException: {str(ex)}")
                    status_text.current.value = f"Exception: {str(ex)}"
                    status_text.current.color = "#FF6B6B"
                finally:
                    decrypt_button.current.disabled = False
                    page.update()

            def update_progress(p):
                progress_bar.current.value = p
                page.update()
                try:
                    print(f"Progress: {p:.1%}", end='\r', flush=True)
                except Exception:
                    pass

            threading.Thread(target=work, daemon=True).start()

        card_border = ft.border.all(1, "#3A4556")
        card_bgcolor = "#1A2332"
        card_radius = 12

        custom_topbar = ft.WindowDragArea(
            content=ft.Container(
                bgcolor="#111922",
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
                content=ft.Row(
                    controls=[
                        ft.Image(src="img/icon.png", width=18, height=18),
                        ft.Text("PyBunga Decryptor", weight=ft.FontWeight.BOLD, size=13, color="#8899AA"),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Icon(ft.Icons.HORIZONTAL_RULE, size=16, color="#8899AA"),
                            width=32, height=32,
                            border=ft.border.all(1, "#3A4556"),
                            border_radius=6,
                            bgcolor="#1A2332",
                            alignment=ft.Alignment(0, 0),
                            on_click=minimize_app,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLOSE, size=16, color="#FF6B6B"),
                            width=32, height=32,
                            border=ft.border.all(1, "#5A2A2A"),
                            border_radius=6,
                            bgcolor="#2A1518",
                            alignment=ft.Alignment(0, 0),
                            on_click=close_app,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                )
            )
        )

        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Pybunga Decryptor",
                    size=34,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.WHITE,
                    width=560,
                ),
                ft.Text(
                    "Digital Eclipse Assets Decryption Tool",
                    size=15,
                    italic=True,
                    text_align=ft.TextAlign.CENTER,
                    color="#8899AA",
                    width=560,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            padding=ft.padding.only(top=12, bottom=16),
        )

        file_config_card = ft.Container(
            content=ft.Column([
                ft.Text("File Configuration", size=13, color="#8899AA", weight=ft.FontWeight.W_500),
                ft.Container(height=4),
                ft.Row([
                    ft.TextField(
                        ref=input_file,
                        label="Input File (.pie)",
                        hint_text="Select input file...",
                        expand=True,
                        read_only=True,
                        border_color="#3A4556",
                        focused_border_color="#64B5F6",
                        label_style=ft.TextStyle(color="#8899AA"),
                        text_style=ft.TextStyle(color=ft.Colors.WHITE),
                        hint_style=ft.TextStyle(color="#556677"),
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("SELECT PIE", weight=ft.FontWeight.BOLD, size=13),
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=pick_input_file,
                        style=ft.ButtonStyle(
                            color="#1A2332",
                            bgcolor="#C8D6E5",
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(horizontal=16, vertical=14),
                        ),
                    ),
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.TextField(
                    ref=output_file,
                    label="Output File",
                    border_color="#3A4556",
                    focused_border_color="#64B5F6",
                    label_style=ft.TextStyle(color="#8899AA"),
                    text_style=ft.TextStyle(color=ft.Colors.WHITE),
                ),
            ], spacing=6),
            padding=16,
            border=card_border,
            border_radius=card_radius,
            bgcolor=card_bgcolor,
        )

        keys_card = ft.Container(
            content=ft.Column([
                ft.Text("Decryption Keys", size=13, color="#8899AA", weight=ft.FontWeight.W_500),
                ft.Container(height=4),
                ft.Row([
                    ft.Dropdown(
                        ref=key_dropdown,
                        label="Select Game Key",
                        value="cowabunga",
                        options=[ft.dropdown.Option(k) for k in KEYS.keys()],
                        expand=True,
                        border_color="#3A4556",
                        focused_border_color="#64B5F6",
                        label_style=ft.TextStyle(color="#8899AA"),
                        text_style=ft.TextStyle(color=ft.Colors.WHITE),
                    ),
                    ft.TextField(
                        ref=custom_key,
                        label="Custom Hex Key",
                        hint_text="Enter hex key here...",
                        expand=True,
                        border_color="#3A4556",
                        focused_border_color="#64B5F6",
                        label_style=ft.TextStyle(color="#8899AA"),
                        text_style=ft.TextStyle(color=ft.Colors.WHITE),
                        hint_style=ft.TextStyle(color="#556677"),
                    ),
                ], spacing=12),
            ], spacing=6),
            padding=16,
            border=card_border,
            border_radius=card_radius,
            bgcolor=card_bgcolor,
        )

        action_section = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.ElevatedButton(
                        ref=decrypt_button,
                        content=ft.Text("Decrypt Now", size=16, weight=ft.FontWeight.BOLD),
                        icon=ft.Icons.LOCK_OPEN,
                        on_click=start_decryption,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor="#2196F3",
                            shape=ft.RoundedRectangleBorder(radius=24),
                            padding=ft.padding.symmetric(horizontal=40, vertical=16),
                            shadow_color="#2196F3",
                            elevation=6,
                        ),
                    ),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=4),
                ft.ProgressBar(ref=progress_bar, value=0, height=8, border_radius=4, color="#2196F3", bgcolor="#1A2332"),
                ft.Container(height=2),
                ft.Text(
                    ref=status_text,
                    value="Ready for Decryption",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color="#8899AA",
                    weight=ft.FontWeight.W_500,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            border_radius=ft.border_radius.only(bottom_left=12, bottom_right=12),
            bgcolor="#111922",
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    custom_topbar,
                    header,
                    ft.Container(
                        content=ft.Column([
                            file_config_card,
                            ft.Container(height=8),
                            keys_card,
                        ]),
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    ft.Container(height=8),
                    action_section,
                ], spacing=0),
                bgcolor="#0D1117",
                expand=True,
                border_radius=12,
            )
        )

    ft.app(target=main, assets_dir=".")

if __name__ == "__main__":
    run_ui()
