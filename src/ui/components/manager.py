import flet as ft

class LayoutManager:
    def __init__(self, content_container: ft.Container, page: ft.Page):
        self.content_container = content_container
        self.page = page
        self.views_cache = {}
        
        # ? Picker Configuration.
        self.picker = ft.FilePicker(on_result=self._handle_picker_result)
        self.page.overlay.append(self.picker)
        self.current_callback = None
        
        # ? Preload views to prevent lag.
        self._init_views()

    def _init_views(self):
        """Initializes all views in cache"""
        from ui.views.converter_view import ConverterView
        from ui.views.downloader_view import DownloaderView
        from ui.views.home_view import HomeView

        self.views_cache = {
            "home": HomeView(self),
            "converter": ConverterView(),
            "media_downloader": DownloaderView(self),
            # Adicione "tasks" aqui se já tiver a view criada
        }

    def _handle_picker_result(self, e: ft.FilePickerResultEvent):
        if e.path and self.current_callback:
            self.current_callback(e.path)
            self.current_callback = None
        self.page.update()

    def open_dir_picker(self, callback):
        self.current_callback = callback
        self.picker.get_directory_path()

    def change_view(self, scene_name):
        # ? Normalize view names to avoid case-sensitivity issues.
        scene_key = scene_name.lower().replace(" ", "_")
        new_view = self.views_cache.get(scene_key)

        if new_view:
            # ? Reset the view to retrigger animations or state changes.
            if hasattr(new_view, "reset_state"):
                new_view.reset_state() 

            # ? Update background.
            self.content_container.image = ft.DecorationImage(
                src=f"assets/backgrounds/{scene_key}.png",
                fit=ft.ImageFit.COVER,
                opacity=0.3
            )

            self.content_container.content = new_view
            
            # ? Global Update - Ensure Flet render the changes.
            self.content_container.update()
            self.page.update()
        else:
            print(f"Erro: View '{scene_key}' not found.")