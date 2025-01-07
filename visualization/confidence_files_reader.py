from random import randint
import pandas as pd         #for reading csv files

table = None
files = ["efficientnet_l2.csv", "efficientnetv2.csv", "openclip_mod_v2_class_names_on_val.csv", "test_5nn.csv"]
group1 = ["efficientnet_l2.csv", "efficientnetv2.csv"] #Empty DataFrame, but why
group2 = ["openclip_mod_v2_class_names_on_val.csv", "test_5nn.csv"]

def choose_file():
    return group2[randint(0, 1)]

def choose_class():
    return randint(0, 999)

def load_table(confidence_file_name):
    return pd.read_csv(f"/home//salat/PycharmProjects/dataset-error-detection/confidences/{confidence_file_name}")















if __name__ == '__main__':
    file_name = choose_file()
    table = load_table(file_name)
    class_num = choose_class()
    print(f"Chosen class: {class_num}")
    print(f"Chosen file: {file_name}")
    print(table.query(f'original_label == {class_num}'))