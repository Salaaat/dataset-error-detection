from random import randint
import confidence_files_reader as cfr
import pandas as pd

from visualization.confidence_files_reader import table

file_num = randint(2, 3)
file_name, file_dict = cfr.choose_file(file_num)
table = cfr.load_table(file_name)
class_num = 208 #cfr.choose_class()
print(f"Chosen class: {class_num}")
print(f"Chosen file: {file_name}")
print(table.query(f'original_label == {class_num}'))


def find(probability_limit):
    wrong_images = table.query(f'top_1_pred != {file_dict[1]}')
    chosen_class_table = wrong_images.query(f'original_label == {class_num}')
    names = chosen_class_table['img_id'].tolist()
    return names







if __name__ == "__main__":
    find(30)