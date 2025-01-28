import confidence_files_reader as cfr


file_num = 2  # randint(2, 3)
file_name, file_dict = cfr.get_dictionary_for_file(file_num)
info_table = cfr.load_table(file_name)
print(f"Chosen file: {file_name}")

def find_first_method_results(class_num):
    wrong_images = info_table.query(f'top_1_pred != {file_dict[1]}')
    chosen_class_table = wrong_images.query(f'original_label == {class_num}')
    if chosen_class_table.empty:
        return chosen_class_table
    answer = input("Chcete zobrazit tabulku s obrázky, které splňují kritéria? (ano/ne) ").casefold()
    if answer == "ano" or answer == "a" or answer == "yes" or answer == "y":
        print(chosen_class_table)
    return chosen_class_table