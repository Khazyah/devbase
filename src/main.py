import flet as ft
import time
from sys import path as syspath
from os import path

# Add parent directory to path to recognize the src folder
syspath.append(path.abspath(path.join(path.dirname(__file__), '..')))

from ui.components.sidebar import SideBar
from ui.components.manager import LayoutManager

def main(page: ft.Page):
    # 1. Window Configuration
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.window.visible = False  # Hide to prevent resize "flash" effect
    
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#202020"

    # 2. Main Container (Will be UNIQUE and managed by LayoutManager)
    # Create with final styling (color, borders) from the start
    main_content = ft.Container(
        expand=True,
        bgcolor="#973838",  # Default background color
        border_radius=ft.BorderRadius(top_left=20, top_right=0, bottom_left=0, bottom_right=0),
        alignment=ft.alignment.center
    )

    # 3. Loading Screen
    loading_screen = ft.Column(
        [
            ft.Text("Loading DevTools...", size=20, color="white"),
            ft.ProgressBar(width=300, color="blue", bgcolor="#333333"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Set loading screen as initial content and show the page
    main_content.content = loading_screen
    page.add(main_content)
    
    page.update()
    page.window.center()
    page.window.visible = True
    page.update()

    # 4. Initialize LayoutManager (Caches all views here)
    manager = LayoutManager(content_container=main_content, page=page)
    time.sleep(1)  # Brief initialization delay
    
    # 5. Assemble Final Layout
    sidebar = SideBar(page, on_change_scene=manager.change_view)
    
    # Clean page and add final Row layout (Sidebar + MainContent)
    page.clean()
    page.add(
        ft.Row(
            [
                sidebar,
                main_content
            ],
            expand=True,
            spacing=0
        )
    )

    # 6. Load Home View
    manager.change_view("home")
    page.update()

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")