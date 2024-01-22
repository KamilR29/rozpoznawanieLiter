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
                if array_data[i] in trn_values_dict[str(i)][value]:
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
