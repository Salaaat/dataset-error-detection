from random import randint
import pandas as pd
from loader.class_loader import ClassDictionary
import image_displayer


class_dictionary = ClassDictionary()

def run():
    chosen_class = None
    num_of_images = None
    chosen_model = None

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
            print(f"Vyskytl se problém: {e}")

        #choose probability limit

    while not num_of_images:
        try:
            num_of_images = input("Kolik obrázků chcete zobrazit? ")
            if num_of_images == '':
                num_of_images = 50  # všechny chybné ve validační sadě
                print("Zobrazí se tedy všechny chybné obrázky.")
            else:
                num_of_images = int(num_of_images)
            if num_of_images <= 0:
                raise ValueError("Počet obrázků musí být větší než 0.")
        except Exception as e:
            print(f"Vyskytl se problém: {e}")

        if not num_of_images:
            num_of_images = 50 #všechny chybné ve validační sadě
            print("Zobrazí se všechny chybné obrázky.")

    while chosen_model == None:
        try:
            chosen_model = input("Vyberte model jehož predikce využijeme; 0, 1 pro efficientnet (supervised), 2 pro openclip (unsupervised): ")
            if chosen_model != '':
                chosen_model = int()
            if not (chosen_model in [0, 1, 2]):
                chosen_model = 2
                print("Použijeme tedy data openclip modelu.")
        except Exception as e:
            print(f"Vyskytl se problém: {e}")

        if chosen_model == None:
            chosen_model = 2
            print("Použijeme tedy data openclip modelu.")

    label_class_table = pd.read_csv("loader/imagenet2012_classes_label_match.csv")
    class_directory = label_class_table.query(f'original_id == {chosen_class}')
    image_displayer.show_images("../imagenet-1k/val/" + class_directory['pt_name'].values[0], num_of_images, chosen_class, class_name, chosen_model)

while True:
    run()