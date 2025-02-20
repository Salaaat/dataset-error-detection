import pandas as pd

pd.set_option('display.max_columns', None)
table = None
files = ["efficientnet_l2.csv", "efficientnetv2.csv", "openclip_mod_v2_class_names_on_val.csv", "test_5nn.csv"]
group1 = ["efficientnet_l2.csv", "efficientnetv2.csv"] #Empty DataFrame, but why
group2 = ["openclip_mod_v2_class_names_on_val.csv", "test_5nn.csv"]

def get_dictionary_for_file(file_number):
    file_dictionary = None
    if file_number == 0 or 1:
        file_dictionary = ["img_id", "original_id", "original_label", "top_1_pred", "top_1_prob", "top_2_pred", "top_2_prob", "top_3_pred", "top_3_prob", "top_4_pred", "top_4_prob", "top_5_pred", "top_5_prob"]
    if file_number == 2:
        file_dictionary = ["img_id", "original_label", None, "top_1_pred", "top_1_prob", "top_2_pred", "top_2_prob", "top_3_pred", "top_3_prob", "top_4_pred", "top_4_prob", "top_5_pred", "top_5_prob"]
    if file_number == 3:
        file_dictionary = ["img_id", "original_label", None, "top_1_pred", "top_1_prob"]
    return files[file_number], file_dictionary

def load_table(confidence_file_name):
    info_table = pd.read_csv(f"../confidences/{confidence_file_name}")
    return info_table
