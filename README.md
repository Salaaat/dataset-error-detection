# Dataset error detection

This is a project for a high school Informatics final exam 

*<italics>confidences, corrected_labels & visualization\loader* -> credit: https://github.com/klarajanouskova and her team

## Folders

### confidences

> conains of two files with predictions of ImageNet-1k from EfficientNet and one from OpenCLIP

### corrected_labels

> a JSON file/s containing some class labels, carefully corrected by a human

### imagenet-1k

> folder for validation set data in ImageNet notation -> /val/...

### visualization

- *confidence_file_reader.py* reads the selected file with confidences and creates a list with names of all columns contained in the .csv file.
- *evaluator.py* uses the previous file and extracts images matching given criteria.
- *image_displayer.py* uses the previous file and creates a display of images and titles according to given criteria.
- *user_interface.py* lets the user choose the class and number of images to display and runs previous file
- *loader* translates between ImageNet class's number, name and name of it's directory


