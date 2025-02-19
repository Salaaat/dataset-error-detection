from random import randint
import pandas as pd
from loader.class_loader import ClassDictionary
import image_displayer


class_dictionary = ClassDictionary()

def run():
    chosen_class = None
    num_of_images = None

    while not chosen_class:
        try:
            class_input = input("\nNapište číslo třídy, kterou chcete zobrazit (0 - 999 nebo „náhodná“): ").casefold()
            if class_input == "náhodná" or class_input == "nahodna" or class_input == "":
                chosen_class = randint(0, 999)
            else:
                chosen_class = int(class_input)
            class_name = class_dictionary.get_class_name(chosen_class)
            print(f"Zvolená třída: {chosen_class},", class_name)
        except Exception as e:
            print(f"Máme problém: {e}")

        #choose probability limit

    while not num_of_images:
        try:
            num_of_images = int(input("Kolik obrázků chcete zobrazit? "))
            if num_of_images <= 0:
                raise ValueError("Počet obrázků musí být větší než 0.")
        except Exception as e:
            print(f"Máme problém: {e}")

        if not num_of_images:
            num_of_images = 50 #všechny chybné ve validační sadě

    label_class_table = pd.read_csv("../loader/imagenet2012_classes_label_match.csv")
    class_directory = label_class_table.query(f'original_id == {chosen_class}')
    image_displayer.show_images("../imagenet-1k/val/" + class_directory['pt_name'].values[0], num_of_images, chosen_class, class_name)

while True:
    run()