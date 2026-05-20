from typing import Any, Callable, List, Tuple

import flet as ft
from flet.core.gradients import Gradient
from ui.components.manager import LayoutManager

class HomeView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        # LISTA PARA RASTREAR OS CARDS DA TELA
        self.cards: List[ft.Container] = []

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
            ), expand=1,
        )

        self.content = ft.Column(
            controls=[
                self.header_container,
                ft.Divider(height=10, leading_indent=50 ,trailing_indent=50, color="white"),
                self.center_container
            ]
        )

    def reset_state(self):
        """Resetar a home para voltar ao padrão e tirar as animações presas."""
        for card in self.cards:
            card.scale = 1.0
            card.offset = ft.Offset(0, 0)
            card.shadow = None

    def hover_animation(self, e):
        """Animação do hover dos containers (usados como botões)"""
        is_hover = e.data == "true"
        
        e.control.scale = 1.05 if is_hover else 1.0
        e.control.offset = ft.Offset(0, -0.05) if is_hover else ft.Offset(0, 0)
        
        e.control.shadow = ft.BoxShadow(
            blur_radius=20, 
            spread_radius=1, 
            color=ft.colors.with_opacity(0.5, "black")
        ) if is_hover else None
        
        e.control.update()

    def create_device_card(self, name, label, icon):
        """Criação de container em forma de botão."""
        # Proteção contra chaves que ainda não existem no cache
        name_converter = {
            "Tasks": "tasks",
            "Converter": "converter",
            "Video Download": "media_downloader",
            "Calculate": "calculate"
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
            ), expand=True,
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
            
            scale=1.0,
            offset=ft.Offset(0, 0), 
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_offset=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),

            on_click=lambda _: self.manager.change_view(name_converter[name]) if name in name_converter else None,
        )

        # Adiciona o card na lista de rastreio antes de retomar.
        self.cards.append(device_card_container)
        return device_card_container