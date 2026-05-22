from typing import Any, Callable, List, Tuple

import flet as ft
from flet.core.gradients import Gradient

class CalculateView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manger = manager

        self.header_container = ft.Container(
            content=ft.Text(value="Calculate View")
        )

        self.content = ft.Column(
            controls=[
                self.header_container
            ]
        )