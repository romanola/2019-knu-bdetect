import csv
import string
import os

exclude = set(string.punctuation)


def _row_abs(i, n):
    """Considering all 'i' > 'n' as positive and 'i' < 'n' as negative review.
    'i' == 'n' ignore neutral rating.

    :param i: rating
    :param n: neutral value
    :return: '+1' as positive value, '-1' as negative
    """
    if i > n:
        return '+1'
    elif i < n:
        return '-1'
    else:
        return i


def _remove_punctuation(text):
    """Remove punctuation from 'text' variable.

    :param text: string with punctuation
    :return: string without punctuation
    """
    return ''.join(ch for ch in text if ch not in exclude)


def _input_csv(filename):
    """Generator for reading csv files by rows.

    :param filename: path to csv file
    :return: rows of csv file
    """
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            yield row


def rewrite_csv_punctuation(filename):
    """Creating new 'clean' csv file without punctuation.

    :param filename: path to csv file
    :return:
    """
    with open('clean_'+filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_iter = _input_csv(filename)
        csv_iter.__next__()
        for row in csv_iter:
            csv_writer.writerow([row[0], _remove_punctuation(row[1]), _row_abs(int(row[2]), 3)])

    print('Rewriting complete.')


def fetch(filename, category_index, unused_indexes=[]):
    """Formatting data according to sklearn dataset.

    :param filename: path to csv file
    :param category_index: index of column with rating in csv file
    :param unused_indexes: index of unused columns
    :return:
    """
    if 'data' in os.listdir():
        return
    os.makedirs('data')
    if 'clean_'+filename not in os.listdir():
        rewrite_csv_punctuation(filename)

    for i, row in enumerate(_input_csv('clean_'+filename)):
        try:
            os.makedirs('data/'+row[category_index])
        except FileExistsError:
            pass
        with open('data/'+row[category_index]+'/{}.txt'.format(i), 'w') as f:
            del row[category_index]
            for index in unused_indexes:
                del row[index]
            f.writelines(row)
    print('Data extracting complete.')


if __name__ == '__main__':
    # For example rewriting 'amazon_baby.csv' for sklearn dataset.
    # First column is unused, and third is used as category.
    fetch('amazon_baby.csv', 2, [0])
