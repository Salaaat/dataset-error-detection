import matplotlib.pyplot as plt
from PIL import Image
import evalueter as ev


def show_images(images_source_path, number_of_images, class_num, probability_limit):
    images_info = ev.find_first_method_results(class_num)
    file_dictionary = ev.file_dict
    if (number_of_images -1) < len(images_info):
        images_info = images_info[:number_of_images]
    else:
        number_of_images = len(images_info)
    loaded_images = load_images(images_info, images_source_path, file_dictionary)
    titles = create_titles(images_info, [True], file_dictionary, number_of_images)
    display_images(loaded_images, titles, number_of_images)

def load_images(images_info, images_source_path, file_dict):
    images = []
    names = images_info[file_dict[0]].tolist()
    for name in names:
        image_path = f'{images_source_path}/{name}'
        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            print(f"Obrázek '{image_path}' nebyl nalezen. Je cesta k obrázkům zadaná správná?")
            exit()
        images.append(image)

    return images

def create_titles(images_info, requested_title, file_dict, number_of_images): #vyresit jinak?
    #requested title as list of Trues and Falses for subjects in file_dictionary
    titles = []
    title_parts = []

    for idx, i in enumerate(requested_title):
        if i:
            list_of_attributes = images_info[file_dict[idx]].tolist()
            title_parts.append(list_of_attributes)

    for idx in range(number_of_images):
        title = ""
        for part in title_parts:
            title += part[idx]
        titles.append(title)

    print(titles)
    return titles

def display_images(loaded_images, titles, number_of_images: int = 1):
    width = 19.2
    height = 10.8
    max_ncols = 5

    nimages_loaded = len(loaded_images)
    if nimages_loaded == 0:
        print("Obrázky splňující tato kritéria nebyly nalezeny.")
        return
    if number_of_images > nimages_loaded:
        number_of_images = nimages_loaded

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
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    if number_of_images == 1:
        axes.imshow(loaded_images[0])
        axes.axis('off')
    elif nrows == 1 or ncols == 1:
        for i in range(number_of_images):
            axes[i].imshow(loaded_images[i])
            axes[i].axis('off')
    elif nrows < 1 or ncols < 1:
            print("Won't show 0 or less images/number_of_images must be integer.")
            return
    else:
        num_loaded = 0
        for row in range(nrows):
            for col in range(ncols):
                slot = row * max_ncols + col
                if slot < nimages_loaded and num_loaded < number_of_images:
                    axes[row][col].imshow(loaded_images[slot])
                    axes[row][col].set_title(titles[slot])
                axes[row][col].axis('off')
                num_loaded += 1

    plt.show()