import confidence_files_reader as cfr
import json
import os
import pandas as pd


corrected_labels_files = ["corrected_labels_val_72_73_74_77_815_76_75.json",
                          "corrected_labels_val_356_357_358_359.json"]
corrected_labels_divided = [[72, 73, 74, 77, 815, 76, 75], [356, 357, 358, 359]]
corrected_classes = []
for class_group in corrected_labels_divided:
    for num in class_group:
        corrected_classes.append(num)

def load_model(file_num):
    file_name, file_dict = cfr.get_dictionary_for_file(file_num)
    info_table = cfr.load_table(file_name)
    return file_name, file_dict, info_table

def find_first_method_results(class_num, file_dict, info_table):
    chosen_class_table = info_table[info_table[file_dict['original_label']] == class_num]
    wrong_images = chosen_class_table[chosen_class_table[file_dict['top_1_pred']] != chosen_class_table[file_dict['original_label']]]

    if wrong_images.empty:
        return wrong_images

    answer = input("Chcete zobrazit tabulku s obrázky, které splňují kritéria? (ano/ne) ").casefold()

    if answer == "ano" or answer == "a" or answer == "yes" or answer == "y":
        print(wrong_images)

    return wrong_images

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
        df = df.astype({
            'class_num': 'int',
            'true_positives': 'int',
            'false_positives': 'int',
            'false_negatives': 'int',
            'true_negatives': 'int',
            'total': 'int'
        })
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

def evaluate_data(class_num_ed, method_results_ed, file_dict_ed, file_name_ed):

    file = ''
    for i in range(len(corrected_labels_files)):
        if class_num_ed in corrected_labels_divided[i]:
            file = corrected_labels_files[i]
            break
    if not file:
        return print(
                f'Opravená data pro vyhodnocení této třídy nejsou k dispozici.\n Zkuste třídy {", ".join([str(i) for i in corrected_classes])}.')

    with open(f"../corrected_labels/{file}", "r") as file:
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
    saving_data(class_num_ed, file_name_ed, new_results)

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

def evaluate_multiple(classes):
    if not classes:
        classes = corrected_classes

    for i in classes:
        if i not in corrected_classes:
            classes = corrected_classes
            break

    files_em = cfr.files

    for model_num in range(len(files_em)):
        file_name, file_dict, info_table = load_model(model_num)
        file_name_ee = files_em[model_num]
        for class_num_ee in classes:
            method_results_ee = find_first_method_results(class_num_ee, file_dict, info_table)
            evaluate_data(class_num_ee, method_results_ee, file_dict, file_name_ee)

    data_dicts = []
    for model in files_em:
        with open(f"../resultes/{model.split('.')[0]}_results.csv", "r") as file:
            df = pd.read_csv(file)
            data_dict = df.to_dict()
            data_dicts.append(data_dict)

    all_data = {"efficientnet_l2": {}, "efficientnetv2": {}, "openclip": {}}
    for idx, data in enumerate(data_dicts):
        model = ["efficientnet_l2", "efficientnetv2", "openclip"][idx]
        for key, list_of_values in data.items():
            all_data[model][key] = int(sum(list_of_values.values()))
        all_data[model]["sensitivity"] = 0
        all_data[model]["specificity"] = 0

    df = pd.DataFrame(all_data)

    for model in files_em:
        model = model.split('.')[0]
        true_positives = df.loc["true_positives", model]
        false_positives = df.loc["false_positives", model]
        false_negatives = df.loc["false_negatives", model]
        true_negatives = df.loc["true_negatives", model]

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
        df.loc["sensitivity", model] = sensitivity
        df.loc["specificity", model] = specificity
    labels_pd = ['class_num', 'true_positives', 'false_positives', 'false_negatives', 'true_negatives', 'total', 'sensitivity', 'specificity']
    df['value_name'] = labels_pd
    df = df[df['value_name'] != 'class_num']
    df.to_csv("../resultes/all_results.csv", index=False)

if __name__ == "__main__":
    #evaluate_multiple([72, 73, 74, 75, 76, 77, 815]) # pavouci, pavucina
    #evaluate_multiple([356, 357, 358, 359]) # fretky, tchori, lasicky
    evaluate_multiple([]) # vsechny opravene tridy
    pass