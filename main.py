import random

from gaussianBayes import naive_bayes_sklearn
from knn import knn_sklearn
from naive_bayes import naive_bayes

filename = "letter-recognition-normalized"
extension = ".data"

def read_data():
    file = open(filename + extension)
    lines = file.readlines()
    file.close()
    return lines

def write_result(result):
    file = open("result_file", "w")
    file.write(result)

def normalize_and_save_data(file_name,normalized_filename):
    file = open(file_name)
    data = file.readlines()
    normalized_data = []

    with open(normalized_filename, "w") as normalized_file:
        for line in data:
            array_data = line.split(',')
            letter = array_data[0]
            normalized_line = [letter]

            for value in array_data[1:]:
                normalized_line.append(float(value))  # Konwertuj na float
            # Normalizuj wartości atrybutów do zakresu (0,1)
            min_val = min(normalized_line[1:])
            max_val = max(normalized_line[1:])
            normalized_values = [(x - min_val) / (max_val - min_val) for x in normalized_line[1:]]
            normalized_line[1:] = normalized_values

            # Zapisz znormalizowany wiersz do pliku
            normalized_file.write(",".join(map(str, normalized_line)) + "\n")

def split_data(lines):
    file_name = "letter-recognition_trn.data"
    names = file_name
    file_trn = open(file_name, "w")
    file_name = "letter-recognition_tst.data"
    names = names + "," + file_name
    file_tst = open(file_name, "w")

    random.shuffle(lines)

    total_lines = len(lines)
    lines_70 = int(total_lines * 0.8)

    for idx, line in enumerate(lines):
        if idx < lines_70:
            file_trn.write(line)
        else:
            file_tst.write(line)

    return names

if __name__ == '__main__':
    normalize_and_save_data("letter-recognition.data", "letter-recognition-normalized.data")
    lines = read_data()

    names = split_data(lines)
    names_tab = names.split(",")

    accuracy = naive_bayes(names_tab[0], names_tab[1])
    accuracy = knn_sklearn(names_tab[0], names_tab[1], 3)
    accuracy = naive_bayes_sklearn(names_tab[0], names_tab[1])
    final_string = "Accuracy: " + str(accuracy) + "\n"
    print("Accuracy: " + str(accuracy))

    write_result(final_string)