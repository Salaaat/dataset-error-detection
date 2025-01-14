from random import randint
from loader import class_loader
from loader.class_loader import ClassDictionary

class_dictionary = ClassDictionary()
def run():
    try:
        class_input = input("Napište číslo třídy, kterou chcete zobrazit (0 - 999 nebo 'náhodná'): ")
        if class_input == "náhodná" or class_input == "nahodna" or class_input == "":
            chosen_class = randint(0, 999)
        else:
            chosen_class = int(class_input)
        print(f"Zvolená třída: {chosen_class},", class_dictionary.get_class_name(chosen_class))
        #choose probability limit
    except Exception as e:
        print(f"An error occurred: {e}")



while True:
    run()