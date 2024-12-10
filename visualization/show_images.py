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

def display_images(loaded_images, number_of_images: int = 1):
    width = 10
    height = 6
    max_ncols = 5

    if number_of_images <= 0:
        nrows, ncols = 1, 1
    elif number_of_images <= max_ncols:
        ncols = number_of_images
        nrows = 1
    else:
        ncols = max_ncols
        nrows = number_of_images // max_ncols

    if number_of_images % max_ncols and not number_of_images <= max_ncols:
        nrows += 1

    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))

    if nrows == 1 or ncols == 1:
        for i in range(number_of_images):
            axes[i].imshow(loaded_images[i])
    elif nrows < 1 or ncols < 1:
        print("Won't show 0 or less images/number_of_images must be integer.")
        exit()
    else:
        pass

    plt.show()


if __name__ == '__main__':
    nms = ['ILSVRC2012_val_00002207.JPEG', 'ILSVRC2012_val_00009208.JPEG', 'ILSVRC2012_val_00000921.JPEG', 'ILSVRC2012_val_00008963.JPEG', 'ILSVRC2012_val_00014741.JPEG', 'ILSVRC2012_val_00017196.JPEG']
    img_scr_path = "/media/salat/disk/imagenet/val/n01496331"
    loaded = load_images(nms, img_scr_path)
    display_images(loaded, 9)