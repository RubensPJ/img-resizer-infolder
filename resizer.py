from PIL import Image
import os
import threading

def resize_and_compress_image(input_path, output_path, target_size=2 * 1024 * 1024, quality=80):
    # Abre a imagem
    img = Image.open(input_path)


    # Calcula o fator de redimensionamento para atingir o tamanho de destino
    width, height = img.size
    current_size = os.path.getsize(input_path)
    scale_factor = (target_size / current_size) ** 0.5

    # Redimensiona a imagem
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Rotaciona a imagem de volta para a orientação original
    img = img.rotate(-90, expand=True)

    # Salva a imagem redimensionada e comprimida
    img.save(output_path, optimize=True, quality=quality)

def process_images_in_directory(directory, target_size=2 * 1024 * 1024, quality=80):
    # Cria um diretório para rastrear as imagens processadas
    processed_dir = os.path.join(directory, 'processed_images')
    os.makedirs(processed_dir, exist_ok=True)

    # Carrega a lista de imagens já processadas
    processed_images = set(os.listdir(processed_dir))

    # Lista de arquivos no diretório
    files = os.listdir(directory)

    # Lista de threads
    threads = []

    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.getsize(file) > target_size and file not in processed_images:
            input_path = os.path.join(directory, file)
            output_path = os.path.join(processed_dir, file)

            thread = threading.Thread(target=resize_and_compress_image, args=(input_path, output_path, target_size, quality))
            thread.start()
            threads.append(thread)

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    current_directory = os.getcwd()  # Obtém o diretório atual

    process_images_in_directory(current_directory)
