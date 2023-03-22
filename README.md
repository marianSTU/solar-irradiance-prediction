## Short documentation
This code is a set of functions that work together to merge a sequence of images into one image. The images are named with a specific format, and the function control_sequence_existence checks if the sequence of images is complete and ready for merging. The images are merged using the function merger and then saved as a new image.

The code uses the following libraries:

PIL for handling images.
logging and coloredlogs for logging messages with colors.
datetime for handling date and time data.
csv for reading data from CSV files.
os for checking if a file exists.
The code starts by defining some constants such as the number of images in the sequence, the month, the year, the exposure time, and the image size. It also defines some paths and the name of the final image.

The first function, explore_csv, takes a filename and a rowname as input and returns a tuple containing the values of 'PictureName', 'Irradiance', and 'DateTime' of the row where the 'PictureName' matches the given rowname. The second function, explore_csv_irr, takes a filename and a rowname as input and returns the value of 'Irradiance' of the row where the 'PictureName' matches the given rowname.

The function get_next_filename takes a filename and a time_next (in minutes) and computes the next date string by adding the given time_next to the current date string. It then returns a new filename that consists of the location, next date, and end string.

The function control_sequence_existence takes a filename and checks if the corresponding original data file exists. If it does, the function continues checking for the existence of the next 5 files with 15 minute intervals between them. If all 5 files exist, the function returns the original filename. If any file is missing, the function continues to search for the next 5 files. If the end file is reached and all files are present, the function returns 'EOF'.

Finally, the function merger takes a filename and a csv writer and merges the sequence of images starting from the given filename. It saves the merged image as a new image.