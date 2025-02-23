import confidence_files_reader as cfr
import json
import os
import pandas as pd

def load_model(file_num):
    file_name, file_dict = cfr.get_dictionary_for_file(file_num)
    info_table = cfr.load_table(file_name)
    return file_name, file_dict, info_table

def find_first_method_results(class_num, file_dict, info_table):
    wrong_images = info_table.query(f'top_1_pred != {file_dict["original_label"]}')
    chosen_class_table = wrong_images.query(f"original_label == {class_num}")
    if chosen_class_table.empty:
        return chosen_class_table
    answer = input("Chcete zobrazit tabulku s obrázky, které splňují kritéria? (ano/ne) ").casefold()
    if answer == "ano" or answer == "a" or answer == "yes" or answer == "y":
        print(chosen_class_table)
    return chosen_class_table

def saving_data(class_num_sd, file_name_sd, new_row):
    model_name = file_name_sd.split(".")[0]
    dir_path = '../resultes'
    save_file_path = f'{dir_path}/{model_name}_results.csv'

    # if not dir: create it
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # if not file: create it
    if not os.path.exists(save_file_path):
        labels_pd = ['class_num', 'true_positives', 'false_positives', 'false_negatives', 'true_negatives', 'total']
        data = {key: [] for key in labels_pd}
        df = pd.DataFrame(data)
    else:
        df = pd.read_csv(save_file_path)

    # copy, rewrite, resave
    if not df['class_num'].isin([class_num_sd]).any():
        df = df._append(new_row, ignore_index=True)

    df = df.sort_values(by=['class_num'])
    df.to_csv(save_file_path, index=False)

def is_image_correctly_labeled(image_true_class, class_number, label_type):
    if label_type == "basic":
        if image_true_class == class_number:
            return True
        else:
            return False
    elif label_type == "multilabel":
        if class_number in image_true_class:
            return True
        else:
            return False
    elif image_true_class == "custom":
        return False
    else:
        return False
    # what to do with uncertain pictures

def evaluate_data(class_num_ed, method_results_ed, file_dict_ed):
    corrected_classes = [72, 73, 74, 75, 76, 77, 815]
    if class_num_ed not in corrected_classes:
        return print(f'Opravená data pro vyhodnocení této třídy nejsou k dispozici.\n Zkuste třídy {", ".join([str(i) for i in corrected_classes])}.')

    with open("../corrected_labels/corrected_labels_val_72_73_74_77_815_76_75.json", "r") as file:
        corrected = json.load(file)

    correct = 0
    wrong = 0
    for image, value in corrected.items():
        if value["old_label"] != class_num_ed:
            continue
        img_true_class = value["new_label"]
        img_type = corrected[image]["label_type"]

        if is_image_correctly_labeled(img_true_class, class_num_ed, img_type):
            correct += 1
        else:
            wrong += 1

    true_positives = 0 #skutečně chybné
    false_positives = 0 #špatně označené jako chybné
    true_negatives = 0 #správně určené jako nechybné
    false_negatives = 0 #špatně určené jako nechybné

    for img in method_results_ed[file_dict_ed["id"]]:
        img_true_class = corrected[img]["new_label"]
        img_type = corrected[img]["label_type"]

        if is_image_correctly_labeled(img_true_class, class_num_ed, img_type):
            false_positives += 1
        else:
            true_positives += 1

    found_as_wrong = len(method_results_ed[file_dict_ed["id"]]) #celkem označených jako chybné
    false_negatives = wrong - true_positives
    true_negatives = correct - false_positives

    if (true_positives + false_negatives) == 0:
        sensitivity = 100
    else:
        sensitivity = 100 * true_positives / (true_positives + false_negatives)
        sensitivity = int(sensitivity - (sensitivity % 1))
    if (true_negatives + false_positives) == 0:
        specificity = 100
    else:
        specificity = 100 * true_negatives / (true_negatives + false_positives)
        specificity = int(specificity - (specificity % 1))

    new_results = {'class_num': class_num_ed, 'true_positives': true_positives, 'false_positives': false_positives, 'false_negatives': false_negatives, 'true_negatives': true_negatives, 'total': wrong + correct}
    saving_data(class_num_ed, file_name, new_results)

    print(f"""
    Vyhodnocení pro třídu {class_num_ed}:

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
    file_number = 1
    class_num = 80
    file_name, file_dict, info_table = load_model(file_number)
    method_results = find_first_method_results(class_num, file_dict, info_table)
    evaluate_data(class_num, method_results, file_dict)
