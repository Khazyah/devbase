import flet as ft
from typing import Any
from modules.converter.engine import convert_image

class ConverterImageView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        format_dropdown = ft.Dropdown(
            label="Convert to:",
            width=200,
            options=[
                ft.dropdown.Option("PNG"),
                ft.dropdown.Option("JPEG"),
                ft.dropdown.Option("WEBP"),
                ft.dropdown.Option("ICO"),
            ],
            value="PNG"
        )

        self.select_image = ft.Container(
            content=ft.Text(value="Select a Image"),
            bgcolor="#3A3A3A",
            height=500,
            width=500,
            alignment=ft.alignment.center,
            margin=ft.margin.only(left=15),
            border_radius=16
            #padding=ft.padding.only(left=100)
            #expand=True
        )

        self.info_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value="Name: Background_Img1"),
                    ft.Text(value="Format: .png"),
                    ft.Text(value="Date: 13/12"),
                ]
            ), expand=True, bgcolor="green"
        )

        converter_buttons = ft.Row(
            controls=[
                ft.Button(text="T"),
                ft.Button(text="V"),
                format_dropdown
            ]
        )

        self.converter_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField(),
                    converter_buttons
                ]
            ), expand=True, bgcolor="red"
        )

        column_content = ft.Column(
            controls=[
                self.info_container,
                self.converter_container
            ]
        )

        self.content = ft.Row(
            controls=[
                self.select_image,
                column_content
            ], expand=True
        )