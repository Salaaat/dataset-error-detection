import matplotlib.pyplot as plt
from PIL import Image

def show_images(images_source_path, information_source_path, number_of_images):
        pass
        #get list of names out of information source
        #get list of information for each picture
        #loaded_images = load_images(names, images_source_path)

def load_images(names, images_source_path):
        images = []
        for name in names:
            image_path = f'{images_source_path}/{name}'
            image = Image.open(image_path)
            images.append(image)

        return images

if __name__ == '__main__':
        nms = ['ILSVRC2012_val_00000921.JPEG']
        img_scr_path = "/media/salat/disk/imagenet/val/n01496331"
        loaded = load_images(nms, img_scr_path)
        plt.imshow(loaded[0])
        plt.axis('off')
        plt.show()
