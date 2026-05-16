import flet as ft

class LayoutManager:
    def __init__(self, content_container: ft.Container, page: ft.Page):
        self.content_container = content_container
        self.page = page
        self.views_cache = {}
        
        # 1. Configuração do Picker
        self.picker = ft.FilePicker(on_result=self._handle_picker_result)
        self.page.overlay.append(self.picker)
        self.current_callback = None
        
        # 2. Pré-carregar as Views (Evita lag na primeira troca)
        self._init_views()

    def _init_views(self):
        """Inicializa todas as views de uma vez no cache"""
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
        # Normaliza o nome para evitar erros de Case Sensitive (Tasks vs tasks)
        scene_key = scene_name.lower().replace(" ", "_")
        
        new_view = self.views_cache.get(scene_key)

        print(scene_key)

        if new_view:
            # 1. Atualiza o fundo
            # Certifique-se que o arquivo existe: assets/backgrounds/home.png, etc.
            self.content_container.image = ft.DecorationImage(
                src=f"assets/backgrounds/{scene_key}.png",
                fit=ft.ImageFit.COVER,
                opacity=0.3
            )

            # 2. Troca o conteúdo
            self.content_container.content = new_view
            
            # 3. Update Global - Garante que o Flet renderize a mudança
            self.content_container.update()
            self.page.update()
        else:
            print(f"Erro: View '{scene_key}' não encontrada no cache.")

"""class LayoutManager:
    def __init__(self, content_container: ft.Container, page: ft.Page):
        self.content_container = content_container
        self.page = page
        self.views_cache = {}
        
        # 1. Configuração do Picker (Deve vir antes das views para garantir)
        self.picker = ft.FilePicker(on_result=self._handle_picker_result)
        self.page.overlay.append(self.picker)
        self.current_callback = None

    def _handle_picker_result(self, e: ft.FilePickerResultEvent):
        # Se o usuário não cancelar (e.path existe) e houver um pedido pendente
        if e.path and self.current_callback:
            self.current_callback(e.path)
            self.current_callback = None # Limpa para o próximo uso
        self.page.update()

    def open_dir_picker(self, callback):
        self.current_callback = callback
        self.picker.get_directory_path()

    def change_view(self, scene_name):
        # 1. Se a view ainda não está no cache, nós a criamos (Lazy Loading)
        if scene_name not in self.views_cache:
            if scene_name == "converter":
                from ui.views.converter_view import ConverterView
                self.views_cache["converter"] = ConverterView()
            
            elif scene_name == "media_downloader":
                from ui.views.downloader_view import DownloaderView
                self.views_cache["media_downloader"] = DownloaderView(self)
            
            elif scene_name == "home":
                from ui.views.home_view import HomeView
                self.views_cache["home"] = HomeView(self)

        # 2. Pegamos a view do cache (ela certamente existe agora)
        new_view = self.views_cache.get(scene_name)

        if new_view:
            # 3. Atualiza o fundo (Isso pode mudar sempre, sem problemas)
            self.content_container.image = ft.DecorationImage(
                src=f"assets/backgrounds/{scene_name}.png",
                fit=ft.ImageFit.COVER,
                opacity=0.3
            )

            # 4. Troca o conteúdo pelo objeto que já estava na memória
            self.content_container.content = new_view
            self.content_container.update()
            self.page.update()
        """

"""
        def change_view(self, scene_name):
        from ui.views.converter_view import ConverterView
        from ui.views.downloader_view import DownloaderView
        from ui.views.home_view import HomeView

        views = {
            "converter": ConverterView(), 
            "media_downloader": DownloaderView(self),
            "home": HomeView(self),
        }

        new_view = views.get(scene_name)
        if new_view:
            # Atualiza o fundo
            self.content_container.image = ft.DecorationImage(
                src=f"assets/backgrounds/{scene_name}.png",
                fit=ft.ImageFit.COVER,
                opacity=0.3
            )

            # Troca o conteúdo
            self.content_container.content = new_view
            self.content_container.update()"""