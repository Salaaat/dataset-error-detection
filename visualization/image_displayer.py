import matplotlib.pyplot as plt
from PIL import Image
import evaluater as ev
import os


def show_images(images_source_path, number_of_images, class_num, class_name, chosen_model):
    #načte data vybraného modelu
    file_name, file_dict, info_table = ev.load_model(chosen_model)
    #získá obrázky mající na prvním místě jinou predikci jiné tříde než je jejich původní
    images_info = ev.find_first_method_results(class_num, file_dict, info_table)
    #sjednotí počet požadovaných obrázků s počtem nalezených
    if (number_of_images -1) < len(images_info):
        images_info = images_info[:number_of_images]
    else:
        number_of_images = len(images_info)
    #zobrazí tabulku
    ev.evaluate_data(class_num, images_info, file_dict, file_name)
    if os.path.exists(images_source_path):
        #načte obrázky
        loaded_images = load_images(images_info, images_source_path, file_dict)
        #vytvoří popisky
        ############################################# file dict
        titles = create_titles(images_info, ["id", "top_1_pred", "top_1_prob"], file_dict, number_of_images)
        #zobrazí obrázky
        display_images(loaded_images, titles, number_of_images, class_name)
    else:
        print(f"Složka {images_source_path} s obrázky z třídy {class_num, class_name} neexistuje.")

def load_images(images_info, images_source_path, file_dict):
    images = []
    #vytvoří seznam názvů
    names = images_info[file_dict["id"]].tolist()
    #načte obrázky podle zadané cesty a názvů
    for name in names:
        image_path = f'{images_source_path}/{name}'
        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            print(f"Obrázek '{image_path}' nebyl nalezen. Je zadaná cesta správně?")
            exit()
        images.append(image)

    return images

def create_titles(images_info, requested_title, file_dict, number_of_images): #vyresit jinak?
    #requested_title je class_group True a False, kde každé pozice odpovídá pozici ve file_dict
    #součástí popisku budou ty, ktere májí na své pozici True
    titles = []
    title_parts = []
    line_names = []

    #podle requested_title se vybere ty atributy, které jsou požadovány k zobrazení
    for key in requested_title:
        try:
            list_of_attributes = images_info[file_dict[key]].tolist()
            title_parts.append(list_of_attributes)
            line_names.append(key)
        except KeyError as e:
            print(f"Popisek nebude obsahovat {key}.") #predelat na slovnik 52, 46-49, 39, 19 a ev

    #všechny popisky poskládá z vybraných atributů
    for idx in range(number_of_images):
        title = ""
        for part in title_parts:
            title += line_names[title_parts.index(part)] + ": "
            title += str(part[idx]) + "\n"
        titles.append(title)

    return titles

def display_images(loaded_images, titles, number_of_images, class_name):
    width = 19.2
    height = 10.8
    max_ncols = 5

    nimages_loaded = len(loaded_images)

    #zkontroluje množství obrázků pro zobrazení
    if nimages_loaded == 0:
        print("Obrázky splňující tato kritéria nebyly nalezeny.")
        return
    if number_of_images > nimages_loaded:
        number_of_images = nimages_loaded

    #nastaví počet řádků a sloupců podle počtu obrázků
    if number_of_images <= 0:
        nrows, ncols = 1, 1
    elif number_of_images <= max_ncols:
        ncols = number_of_images
        nrows = 1
    else:
        ncols = max_ncols
        nrows = number_of_images // max_ncols

    #přidá řádek, pokud počet brázků není dělitelný počtem sloupců a je větší než počet sloupců
    if number_of_images % max_ncols and not number_of_images <= max_ncols:
        nrows += 1

    #připraví okno
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))
    fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.05, hspace=0.5, wspace=0.3)
    fig.suptitle(class_name, fontsize=16)

    #podle množství obrázků je zobrazí
    if number_of_images == 1:
        axes.imshow(loaded_images[0])
        axes.set_title(titles[0])
        axes.axis('off')
    elif nrows == 1 or ncols == 1:
        for i in range(number_of_images):
            axes[i].imshow(loaded_images[i])
            axes[i].set_title(titles[i])
            axes[i].axis('off')
    elif nrows < 1 or ncols < 1:
            print("Nelze zobrazit 0 a méně obrázků.")
            return
    else:
        num_loaded = 0
        for row in range(nrows):
            for col in range(ncols):
                slot = row * max_ncols + col
                if slot < nimages_loaded:
                    axes[row][col].imshow(loaded_images[slot])
                    axes[row][col].set_title(titles[slot])
                axes[row][col].axis('off')
                num_loaded += 1

    plt.show()