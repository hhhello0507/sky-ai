from PIL import Image
import os
from pillow_heif import register_heif_opener

register_heif_opener()
lib_name = 'image_resizer'

join = os.path.join

input_path = join(os.getcwd(), lib_name, 'input_image')
output_path = join(os.getcwd(), lib_name, 'output_image')

images_path = os.listdir(input_path)

output_name = 'normal'

for (idx, image_path) in enumerate(images_path):
    # print(image_path)
    image = Image.open(join(input_path, image_path))
    resized_image = image.resize((640, 480))
    resized_image.save(join(output_path, f'{output_name}_{idx}.jpg'))