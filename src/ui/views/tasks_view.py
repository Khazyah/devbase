import flet as ft

class TaskView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.header_container = ft.Container(
            content=ft.Text(
                value="Tasks",
                size=42,
                font_family="Cascadia Code",
                italic=True,
            ),
            bgcolor="Red",
            #expand=1,
            height=200,
            padding=ft.padding.only(top=50),
            alignment=ft.alignment.center
        )

        text_field = ft.TextField(
            label="Your New Task...",
            border_radius=15,
            width=400,
            bgcolor="#202020",
            border_color="#202020"
        )
        add_button = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="#202020",
            icon_size=30,
            width=50, 
            height=45,
        )

        self.task_add = ft.Container(
            content=ft.Row(
                controls=[text_field, add_button],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor="Green",
            alignment=ft.alignment.center
            #expand=0
        )

        self.task_types = ft.Container(
            content=None,
            bgcolor="Blue",
            #expand=0
        )

        self.tasks = ft.Container(
            content=None,
            bgcolor="Yellow",
            #expand=1
        )

        self.content = ft.Column(
            controls=[
                self.header_container,
                self.task_add,
                self.task_types,
                self.tasks
            ],
            expand=True, spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )