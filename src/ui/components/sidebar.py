import flet as ft

class SideBar(ft.Container):
    def __init__(self, page_reference: ft.Page, on_change_scene):
        super().__init__()
        self.main_page = page_reference
        self.on_change_scene = on_change_scene  # Callback for scene changes
        
        self.width = 58
        self.bgcolor = "#202020"
        self.animate = ft.Animation(400, ft.AnimationCurve.DECELERATE)
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = ft.padding.only(left=10, top=20)
        
        # ? Navigation button list for easy toggle
        self.nav_buttons = [
            self.create_nav_button(ft.Icons.HOME, "Home", "home"),
            self.create_nav_button(ft.Icons.TASK_ALT, "Tasks", "tasks"),
            self.create_nav_button(ft.Icons.CALCULATE, "Calculate", "calculate"),
            self.create_nav_button(ft.Icons.SYNC, "Converter", "converter"),
            self.create_nav_button(ft.Icons.DOWNLOAD, "Downloader", "media_downloader"),
        ]
        self.settigs_buttons = [
            self.create_nav_button(ft.Icons.PERSON, "Accounts", "none"),
            self.create_nav_button(ft.Icons.SETTINGS, "Config", "config"),
        ]

        tools_buttons_container = ft.Container(
            content=ft.Column(
                controls=[
                    *self.nav_buttons
                ]
            ), bgcolor="transparent", expand=1, padding=ft.padding.only(top=10)
        )

        settings_buttons_container = ft.Container(
            content=ft.Column(
                controls=[
                    *self.settigs_buttons
                ]
            ), bgcolor="transparent", expand=0, padding=ft.padding.only(bottom=10)
        )

        self.content = ft.Column(
            controls=[
                ft.IconButton(ft.Icons.LIST, icon_color="white", on_click=self.toggle),
                ft.Divider(height=10, trailing_indent=10, color="white"),
                tools_buttons_container,
                ft.Divider(height=10, trailing_indent=10, color="white"),
                settings_buttons_container
            ],
            spacing=10,
        )

    def reload_current_view(self):
        """Reload the current view in real-time."""
        import importlib
        import views.downloader_view 
        importlib.reload(views.downloader_view)  # Reloads the Python file at runtime

        self.update()
        self.main_page.update()
        
    def create_nav_button(self, icon, text, scene_key):
        """Create navigation buttons for the sidebar."""
        return ft.TextButton(
            width=40,  # Starts collapsed
            content=ft.Container(
                content=ft.Row([ft.Icon(icon, color="white"), ft.Text(text, color="white")], spacing=20),
                width=160,
            ),
            on_click=lambda _: self.on_change_scene(scene_key) if text != "Accounts" else self.reload_current_view,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.only(left=10)),
        )

    def toggle(self, e):
        """Sidebar expand/collapse animation."""
        is_expanding = self.width == 58
        self.width = 160 if is_expanding else 58

        all_buttons = self.nav_buttons + self.settigs_buttons

        for btn in all_buttons:
            btn.width = self.width - 20
        
        self.update()