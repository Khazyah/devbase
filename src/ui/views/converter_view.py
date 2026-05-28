import flet as ft
from typing import Any
from modules.converter.engine import convert_image

class ConverterImageView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        # @ Left Widgets Containers
        header_text = ft.Text(
            size=42,
            italic=True,
            value="Image Converter",
            font_family="Cascadia Code",
        )

        select_file_contaier = ft.Container(
            content=None,
            bgcolor="green",
            expand=True,
            width=300,
            height=300,
        )

        # @ Dropdowns
        formats = ["PNG", "JPEG", "WEBP", "ICO"]
        format_dropdown = ft.Dropdown(
            label="Convert to:",
            width=200,
            options=[ft.dropdown.Option(q) for q in formats],
            value="PNG"
        )

        # @ Containers
        left_conteiner = ft.Container(
            content=ft.Column(
                controls=[
                    header_text,
                    select_file_contaier
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            bgcolor="blue",
            expand=2
        )

        right_container = ft.Container(
            content=None,
            bgcolor="red",
            expand=1
        )

        self.content = ft.Row(
            controls=[
                left_conteiner,
                right_container
            ], spacing=0
        )
