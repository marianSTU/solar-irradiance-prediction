import logging
import coloredlogs
import requests
import zipfile
import os
import datetime
import shutil
import csv
import xml.etree.ElementTree as Et


YEAR = '2018'
MONTH = '01'
EXPO = '10'
MAX_DAY = 32
LOCATION = 'Bern1'
SAVE = f'{MONTH}_{YEAR}_complete_exposure{EXPO}'
DIR_PATH = f'expo{EXPO}_{LOCATION}{YEAR}'


def init():
    logging.getLogger().setLevel(logging.INFO)
    coloredlogs.install(level='INFO')


def getNewZipName(day):
    if day < 10:
        return f'{LOCATION}_{YEAR}{MONTH}0{day}_03-00-00.zip'
    else:
        return f'{LOCATION}_{YEAR}{MONTH}{day}_03-00-00.zip'


def processResponse(r, zip_name, day, csv_writer):
    logging.info(f'Response status:{r.status_code}')

    if r.status_code != 200:
        return False
        # raise Exception(f'Bad response status code: {r.status_code}')

    if not os.path.exists(f'{DIR_PATH}/{SAVE}'):
        os.mkdir(f'{DIR_PATH}/{SAVE}')
    if not os.path.exists(f'{DIR_PATH}/{SAVE}/original'):
        os.mkdir(f'{DIR_PATH}/{SAVE}/original')

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    open('tmp/tmp.zip', "wb").write(r.content)
    try:
        with zipfile.ZipFile('tmp/tmp.zip', mode='r') as archive:
            for file in archive.namelist():
                if f'ExposureStack_Image_{EXPO}' in file:
                    archive.extract(file, f'{DIR_PATH}/{SAVE}/original')
                if file.endswith('.xml'):
                    archive.extract(file)
                    photo_filename = [match for match in archive.namelist() if f'ExposureStack_Image_{EXPO}' in match][0]
                    writeToCsv(photo_filename, file, csv_writer)
                    os.remove(file)
        shutil.rmtree('tmp')
    except:
        zip_name = getNextFilename(zip_name, 10)
        r = requests.get(f'https://portal.csem.ch:9250/skycam/{LOCATION}/{YEAR}/{MONTH}/{zip_name}',
                         auth=('XXXXX', 'XXXXX'), timeout=10)
        shutil.rmtree('tmp')
        processResponse(r, zip_name, day, csv_writer)

    return True


def writeToCsv(photo_filename, filename, csv_writer):
    with open(filename, 'r') as f:
        tree = Et.fromstring(f.read())
        csv_writer.writerow([
            photo_filename,
            tree.attrib.get('logTime'),
            tree.find('Pyranometer').find('Irradiance').text,
            tree.find('Pyranometer').find('IrradianceNotCompensated').text,
            tree.find('Pyranometer').find('BodyTemperature').text,
            tree.find('Pyranometer').find('RelativeHumidity').text,
            tree.find('Pyranometer').find('HumidityTemp').text,
            tree.find('Pyranometer').find('Pressure').text,
            tree.find('Pyranometer').find('PressureAvg').text,
            tree.find('Pyranometer').find('PressureTemp').text,
            tree.find('Pyranometer').find('PressureTempAvg').text,
            tree.find('Pyranometer').find('TiltAngle').text,
            tree.find('Pyranometer').find('TiltAngleAvg').text,
            tree.find('Pyranometer').find('FanSpeed').text,
            tree.find('Pyranometer').find('HeaterCurrent').text,
            tree.find('Pyranometer').find('FanCurrent').text,
            tree.find('Sun').find('Latitude').text,
            tree.find('Sun').find('Longitude').text,
            tree.find('Sun').find('Azimuth').text,
            tree.find('Sun').find('Zenith').text
        ])


def getNextFilename(filename, time_next):
    logging.info(f'Filename: {filename}')
    filename_split = filename.split('_', maxsplit=1)
    location = filename_split[0]
    date_string = filename_split[1].split('.', maxsplit=1)[0]

    date_datetime = datetime.datetime.strptime(date_string, "%Y%m%d_%H-%M-%S")
    next_date_datetime = date_datetime + datetime.timedelta(seconds=time_next)
    next_date_string = next_date_datetime.strftime("%Y%m%d_%H-%M-%S")

    return location + '_' + next_date_string + '.zip'

def getHour(filename):
    filename_split = filename.split('_', maxsplit=1)
    location = filename_split[0]
    date_string = filename_split[1].split('.', maxsplit=1)[0]

    date_datetime = datetime.datetime.strptime(date_string, "%Y%m%d_%H-%M-%S")
    return date_datetime.hour


def main():
    init()
    day = 1
    zip_name = f'{LOCATION}_{YEAR}{MONTH}01_03-00-00.zip'

    if not os.path.exists(f'{DIR_PATH}/{SAVE}'):
        os.mkdir(f'{DIR_PATH}/{SAVE}')

    csv_file = open(f'{DIR_PATH}/{SAVE}/out_data.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    header = ['PictureName',
              'DateTime',
              'Irradiance',
              'IrradianceNotCompensated',
              'BodyTemperature',
              'RelativeHumidity',
              'HumidityTemp',
              'Pressure',
              'PressureAvg',
              'PressureTemp',
              'PressureTempAvg',
              'TiltAngle',
              'TiltAngleAvg',
              'FanSpeed',
              'HeaterCurrent',
              'FanCurrent',
              'SunLatitude',
              'SunLongitude',
              'SunAzimuth',
              'SunZenith'
              ]
    csv_writer.writerow(header)

    while day != MAX_DAY:
        r = requests.get(f'https://portal.csem.ch:9250/skycam/{LOCATION}/{YEAR}/{MONTH}/{zip_name}',  auth=('XXXXX', 'XXXXXXX'), timeout=10)
        hour = int(getHour(zip_name))
        if processResponse(r, zip_name, f'day{day}', csv_writer):
            zip_name = getNextFilename(zip_name, 900)
        elif 3 <= hour <= 12:
            zip_name = getNextFilename(zip_name, 900)
        else:
            day += 1
            zip_name = getNewZipName(day)
            logging.info(f'New day {day}: {zip_name}')

    csv_file.close()


if __name__ == '__main__':
    main()