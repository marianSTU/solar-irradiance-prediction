# Solar Irradiance Prediction using Deep Neural Network.
[![Python 3.10](https://img.shields.io/badge/Python-3.10-orange)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen)](https://github.com/marianSTU/solar-irradiance-prediction/blob/main/LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11.1-brightgreen)](https://www.tensorflow.org/api_docs)
[![Keras](https://img.shields.io/badge/Keras-API-green)](https://keras.io/guides/functional_api/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5.3-red)](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
[![SkyCam](https://img.shields.io/badge/Dataset-SkyCam-blueviolet)](https://github.com/vglsd/SkyCam)
[![Author](https://img.shields.io/badge/Author-Bc.Marián_Šebeňa-blue)](https://is.stuba.sk/lide/clovek.pl?id=97945;)

### Introduction
This script performs the forecasting of solar irradiance by using a 
combination of LSTM and MLP model. It loads a dataset of meteorological
parameters including solar irradiance, zenith angle, temperature, humidity,
pressure, and hour of the day. The script then preprocesses the data, 
trains the model, and evaluates it on test data.

### Data Reading
Two functions are defined for data reading: read_data() and connect_data().

read_data(month, location) reads a single CSV file for a given month and location. The CSV file is assumed to be in a specific format and directory structure.

connect_data() iterates over all months and locations, calls read_data() for each, and concatenates all the resulting dataframes into a single dataframe.

### Data Preprocessing
The data is preprocessed to create sequences for the LSTM model. The length of each sequence is 6

Cross-day sequences and sequences with irradiance over 1300 are removed. The data is then split into a training set and a test set using a 90/10 split.

All features are then standardized using a StandardScaler from the sklearn library.

### Model Training
The model is defined using the Keras functional API. The model consists of an LSTM layer followed by several dense layers. The input shape for the LSTM is (5, 6), corresponding to the sequence length and number of features.

The model is compiled with the Adam optimizer and mean absolute error (MAE) as the loss function. Three metrics are tracked during training: mean absolute error (MAE), mean absolute percentage error (MAPE), and root mean squared error (RMSE).

Training is performed with early stopping, which stops training if the loss on the validation set does not improve after 5 epochs. The batch size is set to 126 and the model is trained for a maximum of 100 epochs.

### Model Evaluation
The model's performance is evaluated using MAE, RMSE, and MAPE, calculated on both the training and test datasets. Additionally, the coefficient of determination, denoted R^2, is calculated.

Please note that this script assumes a specific directory structure and file format for the input data. Be sure to modify the read_data() function if your data is in a different format or directory structure.

