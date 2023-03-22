from PIL import Image
import logging
import coloredlogs
import datetime
import csv
import os

NUM_OF_SEQUENCE = 5
MONTH = '06'
LAST_DAY = '30'
YEAR = '2018'
EXPO_TIME = '10'
IMAGE_SIZE = 64
ORIGINAL_DATA_PATH = f'summer_exposure{EXPO_TIME}/{MONTH}_{YEAR}_complete_exposure{EXPO_TIME}/original'
DIR_PATH = f'summer_exposure{EXPO_TIME}/{MONTH}_{YEAR}_complete_exposure{EXPO_TIME}'
END_FILE = f'Alpnach_{YEAR}{MONTH}{LAST_DAY}_23-45-00_ExposureStack_Image_{EXPO_TIME}_image.png'


def explore_csv(filename, rowname):
    """
    Given a filename and a rowname, this function opens a CSV file, reads the data as a dictionary,
    and returns the 'PictureName', 'Irradiance', and 'DateTime' of the row where the 'PictureName'
    matches the given rowname.

    Args:
    - filename (str): The name of the CSV file to be opened and read.
    - rowname (str): The value of 'PictureName' used to search for the relevant row.

    Returns:
    - A tuple containing the values of 'PictureName', 'Irradiance', and 'DateTime' of the row
    where the 'PictureName' matches the given rowname.
    """
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['PictureName'] == rowname:
                return row['PictureName'], row['Irradiance'], row['DateTime'].split('.', maxsplit=1)[0]


def explore_csv_irr(filename, rowname):
    """
    Given a filename and a rowname, this function opens a CSV file, reads the data as a dictionary,
    and returns the 'Irradiance' of the row where the 'PictureName' matches the given rowname.

    Args:
    - filename (str): The name of the CSV file to be opened and read.
    - rowname (str): The value of 'PictureName' used to search for the relevant row.

    Returns:
    - The value of 'Irradiance' of the row where the 'PictureName' matches the given rowname.
    """
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['PictureName'] == rowname:
                return row['Irradiance']


def get_next_filename(filename, time_next):
    """
    Given a filename and a time_next, this function extracts the location, date, and end string
    from the filename, computes the next date string by adding the given time_next (in minutes)
    to the current date string, and returns a new filename that consists of the location, next date,
    and end string.

    Args:
    - filename (str): The original filename from which to extract information.
    - time_next (int): The number of minutes to add to the current date in the filename.

    Returns:
    - A new filename that consists of the location, next date, and end string.
    """
    filename_split = filename.split('_', maxsplit=6)
    location = filename_split[0]
    date_string = filename_split[1] + '_' + filename_split[2]
    end_string = filename_split[3] + '_' + filename_split[4] + '_' + filename_split[5] + '_' + filename_split[6]

    date_datetime = datetime.datetime.strptime(date_string, "%Y%m%d_%H-%M-%S")
    next_date_datetime = date_datetime + datetime.timedelta(minutes=time_next)
    next_date_string = next_date_datetime.strftime("%Y%m%d_%H-%M-%S")

    return location + '_' + next_date_string + '_' + end_string


def control_sequence_existence(filename):
    """
    Given a filename, this function checks if the corresponding original data file exists. If it does,
    the function continues checking for the existence of the next 5 files with 15 minute intervals between
    them. If all 5 files exist, the function returns the original filename. If any file is missing, the
    function continues to search for the next 5 files. If the end file is reached and all files are present,
    the function returns 'EOF'.

    Args:
    - filename (str): The name of the original file to start searching for.

    Returns:
    - If all files in the sequence are present, the function returns the original filename.
    - If any file is missing, the function returns the next filename in the sequence that was being searched
    for when the missing file was encountered.
    - If the end of the file sequence is reached and all files are present, the function returns 'EOF'.
    """
    count = 0
    flag = 0
    test = filename
    while True:
        if os.path.exists(f"{ORIGINAL_DATA_PATH}/{test}"):
            if flag == 1 and count == 0:
                filename = test
            test = get_next_filename(test, 15)
            count += 1
            if count == 6:
                return filename
        else:
            flag = 1
            count = 0
            test = get_next_filename(test, 15)
            if test == END_FILE:
                return 'EOF'


def merger(filename, csv_writer):
    """
      Given a filename and a csv writer, this function merges the sequence of images starting from the given
      filename and saves the merged image in the corresponding directory. It also writes the filename, date,
      time, and irradiance of the merged image to a CSV file using the given csv writer.

      Args:
      - filename (str): The name of the original file to start merging from.
      - csv_writer (csv.writer): The csv writer object used to write the filename, date, time, and irradiance
      of the merged image to a CSV file.
      """
    next_sequence_start = filename
    i = 0
    while True:
        print(i)
        filename = next_sequence_start
        filename = control_sequence_existence(filename)

        if filename == 'EOF':
            logging.info(f'SUCCESSFULLY DONE')
            break

        irradiances = []
        images = []

        for y in range(0, NUM_OF_SEQUENCE):
            irradiances.append(explore_csv_irr(f'{DIR_PATH}/out_data.csv', filename))
            image = Image.open(f'{ORIGINAL_DATA_PATH}/{filename}')
            images.append(image.resize((IMAGE_SIZE, IMAGE_SIZE)))
            filename = get_next_filename(filename, 15)
            if y == 1:
                next_sequence_start = filename

        picture_name, irradiance, date_time = explore_csv(f'{DIR_PATH}/out_data.csv', filename)

        info = [picture_name,
                f"{DIR_PATH}/sequences_test/{MONTH}_sequence{i}.png",
                date_time,
                irradiance,
                irradiances[0],
                irradiances[1],
                irradiances[2],
                irradiances[3],
                irradiances[4],
                ]

        new_image = Image.new('RGB', (5 * IMAGE_SIZE, IMAGE_SIZE), (250, 250, 250))

        new_image.paste(images[0], (0, 0))
        new_image.paste(images[1], (IMAGE_SIZE, 0))
        new_image.paste(images[2], (2 * IMAGE_SIZE, 0))
        new_image.paste(images[3], (3 * IMAGE_SIZE, 0))
        new_image.paste(images[4], (4 * IMAGE_SIZE, 0))

        csv_writer.writerow(info)
        new_image.save(f"{DIR_PATH}/sequences_test/{MONTH}_sequence{i}.png")
        logging.info(f'Sequence: {info} successfully saved')
        i += 1


def main():
    """
    This is the main function that controls the merging process. It loops over a range of image numbers and
    calls the 'merger' function for each image. It also initializes the csv writer object and writes the
    header row to the CSV file.
    """
    logging.getLogger().setLevel(logging.INFO)
    coloredlogs.install(level='INFO')
    filename = os.listdir(f'{ORIGINAL_DATA_PATH}/')[0]
    csv_file = open(f'{DIR_PATH}/{MONTH}_{YEAR}_expo{EXPO_TIME}_test.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    header = ['PictureName',
              'Path',
              'DateTime',
              'IrradianceToPredict',
              'IrradianceFirst',
              'IrradianceSecond',
              'IrradianceThird',
              'IrradianceFourth',
              'IrradianceFifth',
              ]
    csv_writer.writerow(header)
    merger(filename, csv_writer)
    csv_file.close()


if __name__ == '__main__':
    main()
