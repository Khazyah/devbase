import yt_dlp
import os
from typing import Callable, Optional

def download_video(
    url: str,
    save_path: str,
    quality: str,
    file_format: str,
    progress_callback: Optional[Callable[[dict], None]] = None,
    cancel_flag: Optional[list] = None
) -> dict:
    """
    Realiza o download utilizando yt-dlp com base nas escolhas da UI.
    
    Args:
        url: URL do vídeo
        save_path: Caminho para salvar o arquivo
        quality: Qualidade desejada (ex: "1080p", "720p")
        file_format: Formato do arquivo (mp4, mp3, wav)
        progress_callback: Função callback para atualizar progresso (recebe dict com status)
        cancel_flag: Lista com flag [False] para cancelar (modify para [True])
    
    Returns:
        dict com status: {"success": bool, "message": str, "filename": str or None}
    """
    
    if not url or not url.strip():
        return {"success": False, "message": "Invalid URL"}
    
    if not os.path.isdir(save_path):
        return {"success": False, "message": f"Invalid Path: {save_path}"}
    
    #height = quality.replace("p", "")
    height = "".join(filter(str.isdigit, quality))
    
    def progress_hook(d):
        """Hook chamado pelo yt-dlp durante o download"""
        if cancel_flag and cancel_flag[0]:
            raise Exception("Download Canceled!")
        
        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
            else:
                percent = 0
                speed = 0
                eta = 0
            
            if progress_callback:
                progress_callback({
                    'status': 'downloading',
                    'percent': percent,
                    'downloaded': downloaded,
                    'total': total,
                    'speed': speed,
                    'eta': eta,
                    'filename': d.get('filename', 'Arquivo desconhecido')
                })
        
        elif d['status'] == 'finished':
            if progress_callback:
                progress_callback({
                    'status': 'finished',
                    'percent': 100,
                    'message': 'Completed!'
                })
        
        elif d['status'] == 'error':
            if progress_callback:
                progress_callback({
                    'status': 'error',
                    'message': 'Erro no download'
                })
    
    ydl_opts = {
        'format': f'bestvideo[height<={height}]+bestaudio/best[height<={height}]' if file_format == "mp4" else 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'quiet': False,
        'no_warnings': False,
    }

    if file_format in ["mp3", "wav"]:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': file_format,
            'preferredquality': height #'192' if file_format == "wav" else '320',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
            info = ydl.download([url])
        
        return {
            "success": True,
            "message": "Success!",
            "filename": info
        }
    
    except Exception as e:
        error_msg = str(e)
        return {
            "success": False,
            "message": f"Donwload Error: {error_msg}",
            "filename": None
        }