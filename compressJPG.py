import os
from PIL import Image, ImageOps

def compress_folder(target_mb=4):
    # Automatically use the "Images" folder in the current directory
    folder_path = os.path.join(os.getcwd(), "Images")

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'Created folder: {folder_path}')
        print('Please add JPG images into the Images folder and run again.')
        return

    target_bytes = target_mb * 1024 * 1024
    output_dir = os.path.join(folder_path, "compressed")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            save_path = os.path.join(output_dir, filename)

            with Image.open(file_path) as img:
                # Preserve orientation from EXIF
                img = ImageOps.exif_transpose(img)

                # Convert to RGB for JPEG compatibility
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                temp_img = img.copy()
                quality = 95

                while True:
                    # Save with current quality
                    temp_img.save(
                        save_path,
                        "JPEG",
                        quality=quality,
                        optimize=True
                    )

                    current_size = os.path.getsize(save_path)

                    # Stop if under target size
                    if current_size <= target_bytes:
                        break

                    # Reduce quality first
                    if quality > 75:
                        quality -= 5
                    else:
                        # Then reduce resolution gradually
                        new_size = (
                            int(temp_img.width * 0.9),
                            int(temp_img.height * 0.9)
                        )

                        temp_img = temp_img.resize(
                            new_size,
                            Image.Resampling.LANCZOS
                        )

                print(
                    f"Compressed {filename}: "
                    f"{os.path.getsize(save_path) / (1024 * 1024):.2f} MB"
                )

# Run automatically
compress_folder(target_mb=4)