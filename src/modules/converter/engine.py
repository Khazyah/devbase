from PIL import Image
import os

def convert_image(input_path: str, output_format: str):
    try:
        # Abre a imagem original
        with Image.open(input_path) as img:
            # Remove a extensão antiga e coloca a nova
            base_path = os.path.splitext(input_path)[0]
            new_path = f"{base_path}.{output_format.lower()}"
            
            # Converte para RGB se for salvar como JPEG (JPEG não aceita transparência/RGBA)
            if output_format.upper() in ["JPG", "JPEG"] and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.save(new_path, output_format.upper())
            return f"Sucesso! Salvo em: {new_path}"
    except Exception as e:
        return f"Erro na conversão: {str(e)}"