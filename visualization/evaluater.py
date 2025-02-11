import confidence_files_reader as cfr
import json

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

def evaluate_data(class_num, method_results):
    corrected_classes = [72, 73, 74, 77, 815, 76, 75]
    if class_num not in corrected_classes:
        return print(f'Opravená data pro vyhodnocení této třídy nejsou k dispozici.\n Zkuste třídy {", ".join([str(i) for i in corrected_classes])}.')

    with open("../corrected_labels/corrected_labels_val_72_73_74_77_815_76_75.json", "r") as file:
        corrected = json.load(file)

    correct = 0 #
    wrong = 0
    for image, value in corrected.items():
        if value["old_label"] != class_num:
            continue
        if value["new_label"] == class_num:
            correct += 1
            continue
        try:
            if class_num in value["new_label"]:
                correct += 1
            else:
                wrong += 1
        except Exception as e:
            pass

    true_positives = 0 #skutečně chybné
    false_positives = 0 #špatně oznacené jako chybné
    true_negatives = 0 #správně určené jako nechybné
    false_negatives = 0 #špatně určené jako nechybné

    for img in method_results[file_dict[0]]:
        """try:
            new_label = corrected[img]["new_label"]  # Extract value once

            if isinstance(new_label, list):  # Handle list case
                if class_num in new_label:
                    true_negatives += 1
                else:
                    false_negatives += 1
            else:  # Handle number case
                if new_label == class_num:
                    true_negatives += 1
                else:
                    false_negatives += 1

        except KeyError:
            print(f"Warning: Image {img} not found in corrected labels.")"""
        '''
        new_label = corrected[img]["new_label"]
        print(type([new_label]))
        if not type(new_label) == "list":
            new_label = [new_label]
        if class_num in new_label:
            true_negatives += 1
        else:
            false_negatives += 1'''

        if corrected[img]["new_label"] == class_num:
            true_negatives += 1
            continue
        try:
            if class_num in corrected[img]["new_label"]:
                true_negatives += 1
            else:
                false_negatives += 1
        except Exception as e:
            pass

    found_as_wrong = len(method_results[file_dict[0]]) #celkem označených jako chybné
    true_positives = wrong - false_negatives
    false_positives = correct - true_negatives

    if true_positives + false_negatives == 0:
        sensitivity = 100
    else:
        sensitivity = 100 * true_positives / (true_positives + false_negatives)
        sensitivity = int(sensitivity - (sensitivity % 1))
    if true_negatives == 0:
        specificity = 0
    else:
        specificity = 100 * true_negatives / (true_negatives + false_positives)
        specificity = int(specificity - (specificity % 1))

    print(f"""
    Vyhodnocení pro třídu {class_num}:

             | chybné | správné | celkem
    -------------------------------------
    označené |\t\t  |\t\t\t |
    jako     | {true_positives}\t  | {false_positives}\t\t | {found_as_wrong}
    chybné   |\t\t  |\t\t\t |
    -------------------------------------
    označené |\t\t  |\t\t\t |
    jako     | {false_negatives}\t  | {true_negatives}\t\t | {false_negatives + true_negatives}
    správné  |\t\t  |\t\t\t |
    -------------------------------------
    celkem   | {wrong}\t  | {correct}\t\t | {wrong + correct}
    
    
    senzitivita = {sensitivity} %
    specificita = {specificity} %

""")



if __name__ == "__main__":
    class_num = 74
    method_results = find_first_method_results(class_num)
    print (method_results)
    evaluate_data(class_num, method_results)