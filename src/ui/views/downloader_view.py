import flet as ft
import threading
import time

from modules.downloader.engine import download_video

class DownloaderView(ft.Container):
    def __init__(self, manager):
        super().__init__()
        self.lbl_path = ft.Text("Nenhuma pasta selecionada", italic=True)
        self.manager = manager
        self.expand = True
        self.download_thread = None
        self.cancel_flag = [False]
        
        # --- Atributos dos Widgets ---
        
        self.header_text = ft.Text(
            value="Media Downloader",
            size=42,
            font_family="Cascadia Code",
            italic=True,
        )

        self.url_input = ft.TextField(
            label="Your media URL...",
            border_radius=15,
            width=500,
            bgcolor="#202020",
            border_color="#202020"
        )

        self.url_input.on_change = lambda _: self.validate_fields()

        self.download_button = ft.Button(
            text="Download",
            color="#FFFFFF",
            bgcolor="#176CBB", 
            height=45, 
            width=120,
            on_click=self.handle_download,
            elevation=0
        )

        self.cancel_button = ft.Button(
            text="Cancelar",
            bgcolor="#C41C3B",
            height=45,
            width=120,
            visible=False,
            on_click=self.handle_cancel,
            elevation=0
        )

        self.file_button = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_color="#ffd04d",
            icon_size=30,
            width=50, 
            height=45, 
            on_click=self.open_file_picker
        )

        self.file_video_quality = ["1080p", "720p", "360p", "120p"]
        self.file_audio_quality = ["320kbps", "256kbps", "192kbps"]
        file_format = ["mp4", "mp3", "wav"]
        
        self.file_format_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(f) for f in file_format], 
            filled=True, 
            border=ft.InputBorder.OUTLINE,
            width=115, 
            border_radius=20, 
            bgcolor="#202020", 
            fill_color="#202020",
            border_color="#202020", 
            value=file_format[0],
            on_change=self.format_on_change
        )
        
        self.file_quality_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(q) for q in self.file_video_quality], 
            filled=True, 
            border=ft.InputBorder.OUTLINE,
            width=115, 
            border_radius=20, 
            bgcolor="#202020", 
            fill_color="#202020",
            border_color="#202020", 
            value=self.file_video_quality[0],
        )

        # Progress Bar
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=500,
            height=15,
            visible=False,
            color="#176CBB",
            bgcolor="#1a1a1a",
            border_radius=20,
        )

        self.progress_text = ft.Text(
            value="",
            size=12,
            color="#FFFFFF",
            visible=False
        )

        self.status_message = ft.Text(
            value="",
            size=12,
            color="#FFFFFF",
            visible=False
        )

        # @ Header Container
        header_container = ft.Container(
            content=self.header_text, 
            alignment=ft.alignment.bottom_center,
            padding=ft.padding.only(bottom=30), 
            expand=1,
        )

        # @ Center Container (URL Input)
        center_container = ft.Container(
            content=ft.Row(
                controls=[self.url_input], 
                alignment=ft.MainAxisAlignment.CENTER
            ), 
            height=48,
        )

        # @ Progress Containers
        self.stack_progress = ft.Stack(
            controls=[
                self.progress_bar,
                ft.Container(
                    content=self.progress_text,
                    expand=True,
                    left=2,
                ),
                ft.Container(
                    content=self.status_message,
                    expand=True,
                    right=8,
                )
            ],
        )

        self.progress_container = ft.Container(
            content=ft.Row(
                controls=[self.stack_progress],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            visible=False,
            #bgcolor="green",
            height=20,
            expand=0,
            alignment=ft.alignment.center,
        )

        # @ Bottom Container
        left_bottom_container = ft.Container(
            content=ft.Row(
                controls=[self.download_button, self.cancel_button, self.file_button], 
                alignment=ft.MainAxisAlignment.END,
            ), 
            expand=True, 
            margin=ft.margin.only(right=65),
        )
        
        right_bottom_container = ft.Container(
            content=ft.Row(
                controls=[self.file_format_dropdown, self.file_quality_dropdown],
                alignment=ft.MainAxisAlignment.START,
            ),  
            expand=True, 
            margin=ft.margin.only(left=6),
        )
        
        bottom_container = ft.Container(
            content=ft.Row(
                controls=[left_bottom_container, right_bottom_container]
            ), 
            expand=True, 
            alignment=ft.alignment.top_center,
        )

        # @ Final Layout
        self.content = ft.Column(
            controls=[
                header_container, 
                center_container,
                self.progress_container,
                bottom_container
            ], 
            expand=True
        )

    # @ --- Métodos de Lógica ---

    def format_on_change(self, e):
        file_quality = self.file_audio_quality if e.control.value in ["wav", "mp3"] else self.file_video_quality
        self.file_quality_dropdown.options = [ft.dropdown.Option(q) for q in file_quality]
        self.file_quality_dropdown.value = file_quality[0]
        self.file_quality_dropdown.update()

    def validate_fields(self):
        url = self.url_input.value or ""
        path = self.lbl_path.value or ""

        if url.strip() != "" and "Nenhuma pasta" not in path:
            self.download_button.disabled = False
        else:
            self.download_button.disabled = True
        self.update()

    def open_file_picker(self, e):
        self.manager.open_dir_picker(self.on_path_result)

    def on_path_result(self, path):
        if path:
            self.lbl_path.value = f"Caminho: {path}"
            self.lbl_path.color = ft.colors.BLUE_200
            self.validate_fields()
        self.update()

    def update_progress(self, data: dict):
        """Callback chamado pelo engine durante o download"""
        status = data.get('status')
        
        # Garantir que progress_bar está visível
        if not self.progress_bar.visible:
            self.progress_bar.visible = True
        if not self.progress_text.visible:
            self.progress_text.visible = True
        
        if status == 'downloading':
            percent = data.get('percent', 0) / 100
            self.progress_bar.value = percent
            
            downloaded = data.get('downloaded', 0)
            total = data.get('total', 0)
            speed = data.get('speed', 0)
            
            # Formatar bytes para MB/GB
            def format_bytes(bytes_val):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if bytes_val < 1024:
                        return f"{bytes_val:.1f}{unit}"
                    bytes_val /= 1024
                return f"{bytes_val:.1f}TB"
            
            # Formatar velocidade
            def format_speed(speed_val):
                if speed_val is None:
                    return "Calculating..."
                return f"{format_bytes(speed_val)}/s"
            
            down_str = format_bytes(downloaded)
            total_str = format_bytes(total)
            speed_str = format_speed(speed)
            
            percent_display = data.get('percent', 0)
            self.progress_text.value = f"{percent_display:.1f}% - {down_str}/{total_str} ({speed_str})"
            
        elif status == 'finished':
            self.progress_bar.value = 1.0
            self.progress_text.value = "Finishing... Compiling Audio..."
        
        self.update()

    def reset_ui(self):
        """Reseta a UI após download"""
        self.download_button.visible = True
        self.cancel_button.visible = False
        self.progress_container.visible = False
        self.status_message.visible = False
        self.progress_bar.value = 0
        self.progress_text.value = ""
        self.download_button.disabled = False
        self.download_button.text = "Download"
        self.download_button.bgcolor = "#176CBB"
        self.update()

    def handle_cancel(self, e):
        """Cancela o download em andamento"""
        self.cancel_flag[0] = True
        self.cancel_button.disabled = True
        self.status_message.value = "Cancelando..."
        self.status_message.color = ft.colors.ORANGE_400
        self.update()

    def handle_download(self, e):
        url = self.url_input.value.strip() if self.url_input.value else ""
        current_path = self.lbl_path.value or ""

        # Validações
        if not url:
            self.status_message.value = "❌ URL is needed!"
            self.status_message.color = ft.colors.RED_400
            self.status_message.visible = True
            self.update()
            return

        if "Nenhuma pasta" in current_path or not current_path:
            self.status_message.value = "❌ Select a folder for download!"
            self.status_message.color = ft.colors.RED_400
            self.status_message.visible = True
            self.update()
            return

        save_path = current_path.replace("Caminho: ", "")
        quality = self.file_quality_dropdown.value
        fmt = self.file_format_dropdown.value

        # Mostrar progress
        self.download_button.visible = False
        self.cancel_button.visible = True
        self.progress_container.visible = True
        self.progress_bar.visible = True
        self.progress_text.visible = True
        self.status_message.visible = False
        self.cancel_flag = [False]
        self.progress_bar.value = 0
        self.progress_text.value = "Starting..."
        self.update()

        # Executar em thread separada para não bloquear UI
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, save_path, quality, fmt),
            daemon=True
        )
        self.download_thread.start()

    def _download_worker(self, url: str, save_path: str, quality: str, fmt: str):
        """Worker thread para executar o download"""
        try:
            result = download_video(
                url=url,
                save_path=save_path,
                quality=quality,
                file_format=fmt,
                progress_callback=self.update_progress,
                cancel_flag=self.cancel_flag
            )

            # Aguardar um pouco para UI atualizar
            time.sleep(0.5)

            # Mostrar resultado
            if result['success']:
                self.status_message.value = f"✅ {result['message']}"
                self.status_message.color = ft.colors.GREEN_400
            else:
                self.status_message.value = f"❌ {result['message']}"
                self.status_message.color = ft.colors.RED_400

            self.status_message.visible = True
            
            # Resetar após 2 segundos
            threading.Timer(3.0, self.reset_ui).start()

        except Exception as err:
            self.status_message.value = f"❌ Error: {str(err)}"
            self.status_message.color = ft.colors.RED_400
            self.status_message.visible = True
            threading.Timer(3.0, self.reset_ui).start()