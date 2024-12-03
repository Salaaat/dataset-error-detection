from unicodedata import digit

import matplotlib.pyplot as plt
from PIL import Image

def show_images(images_source_path, information_source_path, number_of_images):
    pass
    #get list of names out of information source
    #get list of information for each picture
    #loaded_images = load_images(names, images_source_path)
    #dislplay_images(loaded_images, number_of_images)

def load_images(names, images_source_path):
    images = []
    for name in names:
        image_path = f'{images_source_path}/{name}'
        image = Image.open(image_path)
        images.append(image)

    return images

def display_images(loaded_images, number_of_images):
    width = 10
    height = 6
    side_size = int(number_of_images**0.5 // 1)
    columns = side_size
    rows = side_size +1

    fig, axes = plt.subplots(columns, rows, figsize=(width, height))

    for i in range(number_of_images):
        axes[i].imshow(loaded_images[i])

    plt.show()


if __name__ == '__main__':
    nms = ['ILSVRC2012_val_00000921.JPEG', 'ILSVRC2012_val_00002207.JPEG', 'ILSVRC2012_val_00009208.JPEG']
    img_scr_path = "/media/salat/disk/imagenet/val/n01496331"
    loaded = load_images(nms, img_scr_path)
    display_images(loaded, 2)