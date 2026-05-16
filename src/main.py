import flet as ft
import time
from sys import path as syspath
from os import path

# Ajuste de path para reconhecer a pasta src
syspath.append(path.abspath(path.join(path.dirname(__file__), '..')))

from ui.components.sidebar import SideBar
from ui.components.manager import LayoutManager

def main(page: ft.Page):
    # 1. Configurações de Janela
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.window.visible = False # Esconde para evitar o "flash" de redimensionamento
    
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#202020"

    # 2. Container Principal (Ele será ÚNICO e usado pelo Manager)
    # Criamos ele com o estilo final (cor, bordas) desde o início
    main_content = ft.Container(
        expand=True,
        bgcolor="#973838", # Cor de fundo padrão
        border_radius=ft.BorderRadius(top_left=20, top_right=0, bottom_left=0, bottom_right=0),
        alignment=ft.alignment.center
    )

    # 3. Tela de Loading
    loading_screen = ft.Column(
        [
            ft.Text("Loading DevTools...", size=20, color="white"),
            ft.ProgressBar(width=300, color="blue", bgcolor="#333333"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Definimos o loading como conteúdo inicial e mostramos a página
    main_content.content = loading_screen
    page.add(main_content)
    
    page.update()
    page.window.center()
    page.window.visible = True
    page.update()

    # 4. Inicialização do Manager (Aqui ele faz o cache das views)
    # Isso leva um tempinho, por isso o loading está na tela
    manager = LayoutManager(content_container=main_content, page=page)
    time.sleep(1) # Um tempinho de espera. 
    
    # 5. Montagem do Layout Final
    # Agora que o manager carregou, criamos a Sidebar
    sidebar = SideBar(page, on_change_scene=manager.change_view)
    
    # Limpamos a página para colocar a Row definitiva (Sidebar + MainContent)
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

    # 6. Carregamos a Home
    # O change_view vai substituir o loading pelo conteúdo da Home dentro do main_content
    manager.change_view("home")
    page.update()

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")