import random

filename = "letter-recognition"
extension = ".data"



def read_data():
    file = open(filename + extension)
    lines = file.readlines()
    file.close()
    return lines

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

def split_data(lines, number):
    file_name = "letter-recognition_trn" + number + ".data"
    names = file_name
    file_trn = open(file_name, "w")
    file_name = "letter-recognition_tst" + number + ".data"
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


def naive_bayes(trening_file, test_file):
    trn_file = open(trening_file)
    tst_file = open(test_file)

    trn_data = trn_file.readlines()
    tst_data = tst_file.readlines()

    # pętla tworząca słownik wyników  danych treningowych
    trn_dict = {}
    for line in trn_data:
        array_data = line.split(',')
        letter = array_data[0].rstrip("\n")
        if letter in trn_dict.keys():
            value = trn_dict[letter]
            trn_dict[letter] = value + 1
        else:
            trn_dict[letter] = 1

    line_lenght = len(trn_data[0].split(",")) - 1
    # pętla tworząca słownik zliczająca wystąpienia poszczególnych danych w zależnoći od wyniku
    trn_values_dict = {}
    for index in range(1, line_lenght + 1):
        i = str(index)
        trn_values_dict[i] = {}
        for line in trn_data:
            array_data = line.split(",")
            letter = array_data[0].strip("\n")
            if letter in trn_values_dict[i]:
                if array_data[index] in trn_values_dict[i][letter]:
                    value = trn_values_dict[i][letter][array_data[index]]
                    trn_values_dict[i][letter][array_data[index]] = value + 1
                else:
                    trn_values_dict[i][letter][array_data[index]] = 1
            else:
                trn_values_dict[i][letter] = {array_data[index]: 1}

    key_list = []
    for key in trn_dict.keys():
        key_list.append(key)
    # pętla obliczająca prawdopodaobieńśtwo przynależnoći do danej grupy
    final_list = []
    for line in tst_data:
        array_data = line.split(",")
        tmp_tab = []
        for value in trn_dict:
            final_value = 1

            for i in range(1, len(array_data)):
                if (array_data[i] in trn_values_dict[str(i)][value]):
                    tmp = trn_values_dict[str(i)][value][array_data[i]]
                else:
                    tmp = 0

                final_value = final_value * (tmp / trn_dict[value])

            tmp_tab.append(final_value)
        max_value = max(tmp_tab)
        value_index = tmp_tab.index(max_value)

        final_list.append(key_list[value_index])

    iterator = 0
    sum_value = 0
    for line in tst_data:

        array_data = line.split(",")
        letter = array_data[0].strip("\n")

        if letter == final_list[iterator]:
            sum_value = sum_value + 1
        iterator = iterator + 1

    accuracy = sum_value / len(final_list)

    return accuracy


def write_result(result):
    file = open("result_file", "w")
    file.write(result)


if __name__ == '__main__':



    lines = read_data()

    names = split_data(lines, "1")
    names_tab = names.split(",")
    # normalize_and_save_data(names_tab[0],"letter-recognition_trn1.data")
    # normalize_and_save_data(names_tab[1],"letter-recognition_tst1.data")


    accuracy = naive_bayes(names_tab[0], names_tab[1])
    final_string = "Accuracy: " + str(accuracy) + "\n"
    print("Accuracy: " + str(accuracy))

    write_result(final_string)

