import flet as ft
from typing import Any
from modules.converter.engine import convert_image

def ConverterView():
    selected_files_text = ft.Text("Nenhum arquivo selecionado")
    result_text = ft.Text()
    
    # Armazenamos o caminho em uma variável simples para facilitar
    file_path = ""

    format_dropdown = ft.Dropdown(
        label="Converter para:",
        width=200,
        options=[
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("JPEG"),
            ft.dropdown.Option("WEBP"),
            ft.dropdown.Option("ICO"),
        ],
        value="PNG"
    )

    # Usamos on_result para obter o caminho local correto
    def on_file_result(e: Any):
        nonlocal file_path
        if e.files:
            file_path = e.files[0].path
            selected_files_text.value = f"Selecionado: {e.files[0].name}"
            selected_files_text.update()

    file_picker = ft.FilePicker(on_result=on_file_result)

    def handle_convert(e):
        # Garantimos que o valor não é None com um fallback ("PNG")
        target_format = format_dropdown.value if format_dropdown.value else "PNG"
        
        if not file_path:
            result_text.value = "Selecione um arquivo primeiro!"
            result_text.color = "red"
        else:
            result_text.value = "Convertendo..."
            result_text.update()
            
            res = convert_image(file_path, target_format)
            result_text.value = res
            result_text.color = "green" if "Sucesso" in res else "red"
        
        e.page.update()

    header_text = ft.Text("Conversor de Imagem", size=25)
    select_image_button_row = ft.Row(
        controls=[
            ft.Button("Selecionar Imagem", icon=ft.Icons.IMAGE_SEARCH, on_click=lambda _: file_picker.pick_files()),
            format_dropdown
        ]
    )
    converter_button_row = ft.Row(
        controls=[
            ft.Button("Converter Agora", on_click=handle_convert, bgcolor="blue", color="white"),
            result_text
        ]
    )

    final_layout = ft.Column(
        controls=[header_text, select_image_button_row, converter_button_row]
    )

    return final_layout