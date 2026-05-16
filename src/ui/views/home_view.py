from typing import Any, Callable, List, Tuple

import flet as ft
from flet.core.gradients import Gradient
from ui.components.manager import LayoutManager

class HomeView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.header_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="DevTools",
                        color="#FFFFFF",
                        font_family="JetBrains Mono",
                        size=36
                    ),
                    ft.Text(
                        value="A aplication that help you to improve your time, and eficience.",
                        color="#D3D2D2",
                        font_family="Cascadia Code",
                        size=12
                    )
                ], spacing=5
            ), 
            expand=0,
            alignment=ft.alignment.center_left,
            padding=ft.padding.only(left=50, top=50)
            #bgcolor="red"
        )

        self.center_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.create_device_card("Tasks", "Manager your tasks and more", "task_alt"),
                            self.create_device_card("Video Download", "Download any video url", "download")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            self.create_device_card("Converter", "Converter images format", "sync"),
                            self.create_device_card("Calculate", "Calculete your financial life", "calculate")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ), expand=1, #bgcolor="green"
        )

        self.content = ft.Column(
            controls=[
                self.header_container,
                ft.Divider(height=10, leading_indent=50 ,trailing_indent=50, color="white"),
                self.center_container
            ]
        )

    def hover_animation(self, e):
        # e.data == "true" quando o mouse entra, "false" quando sai
        is_hover = e.data == "true"
        
        e.control.scale = 1.05 if is_hover else 1.0
        
        # Correção do Offset: use (0, 0) em vez de None para voltar ao normal
        e.control.offset = ft.Offset(0, -0.05) if is_hover else ft.Offset(0, 0)
        
        # Sombra: blur_radius maior dá mais profundidade
        e.control.shadow = ft.BoxShadow(
            blur_radius=20, 
            spread_radius=1, 
            color=ft.colors.with_opacity(0.5, "black")
        ) if is_hover else None
        
        e.control.update()

    def create_device_card(self, name, label, icon):
        name_converter = {
            "Converter": "converter",
            "Video Download": "media_downloader",
        }

        icon_container = ft.Container(
            content=ft.Icon(name=icon, color="white"),
            height=50, width=50, border_radius=24,
            bgcolor="#333333",
        )
        texts_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(value=name, color="#FFFFFF", size=18, font_family="Cascadia Code"),
                        padding=ft.padding.only(left=10, top=10)
                    ),
                    ft.Container(
                        ft.Text(value=label, color="D3D2D2", size=9, font_family="JetBrains Mono"),
                        padding=ft.padding.only(left=12)
                    )
                ], spacing=0, 
            ), expand=True, #bgcolor="green"
        )

        device_card_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=icon_container,
                        padding=ft.padding.only(left=10, top=15),
                        alignment=ft.alignment.center_left
                    ),
                    texts_container
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH, 
                spacing=0
            ), 
            bgcolor="#1a1a1a", 
            width=170,
            height=175,
            border_radius=20, 
            ink=True, 
            on_hover=self.hover_animation,
            
            # --- AJUSTES DE ANIMAÇÃO ---
            scale=1.0,
            offset=ft.Offset(0, 0), # OBRIGATÓRIO ter valor inicial para animar
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_offset=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),

            on_click=lambda _: self.manager.change_view(name_converter[name]),
        )

        return device_card_container