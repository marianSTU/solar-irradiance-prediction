# Solar Irradiance Prediction using Deep Neural Network.
[![Python 3.10](https://img.shields.io/badge/Python-3.10-orange)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen)](https://github.com/marianSTU/solar-irradiance-prediction/blob/main/LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11.1-brightgreen)](https://www.tensorflow.org/api_docs)
[![Keras](https://img.shields.io/badge/Keras-API-green)](https://keras.io/guides/functional_api/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5.3-red)](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
[![SkyCam](https://img.shields.io/badge/Dataset-SkyCam-blueviolet)](https://github.com/vglsd/SkyCam)
[![Author](https://img.shields.io/badge/Author-Bc.Marián_Šebeňa-blue)](https://is.stuba.sk/lide/clovek.pl?id=97945;)

### Data Reading

The data reading phase involves importing csv data for each month of the year 2018 for a specific location (in this case, Alpnach). This data is found in the csv files contained in each monthly directory of the specified location and includes various meteorological parameters such as irradiance, zenith, hour, pressure, humidity, and temperature. In addition to this, the script reads and processes images related to each timestamp in the csv data. These images are stored in an array for later use.

### Data Preprocessing

The data preprocessing phase consists of splitting the time series data into overlapping sequences of length five. The last element of each sequence is used as the target value for the prediction. Sequences that cross over to a new day or sequences that have a target value above 1300 are removed to maintain consistency in the data.

The preprocessing also involves standardizing the features using Scikit-Learn's StandardScaler. Standardization is a common requirement for machine learning estimators: they might behave badly if the individual features do not more or less look like standard normally distributed data. This is especially true for neural networks.

### Model Building

The script employs a combined CNN-LSTM and LSTM model. CNN is used to extract features from images while LSTM is used to capture temporal dependencies. The extracted image features and the temporal features are then concatenated and passed through a Multi-Layer Perceptron (MLP) for the final prediction.

The image processing part of the model involves a sequence of convolutional layers followed by max pooling layers. The output of these layers is flattened and passed through a dropout layer (for regularization) and two dense layers. This sequence is repeated for each image in the sequence.

On the other hand, the LSTM network is used to process the sequence of meteorological data. The output of the LSTM is passed through a series of dense layers. The outputs of the image processing and meteorological data processing parts are then concatenated and passed through a series of dense layers for the final prediction.

The combined model is trained using the Adam optimizer with an exponential decay schedule for the learning rate. The loss function used is the Mean Absolute Error (MAE), and the model is evaluated using additional metrics such as the Mean Absolute Percentage Error (MAPE) and Root Mean Squared Error (RMSE).

### Model Evaluation

After the model has been trained, it is evaluated on both the training data and the test data. The script calculates the MAE, RMSE, and MAPE for both datasets and also computes the R^2 score, which gives a measure of how well future samples are likely to be predicted by the model.

This script is a full-fledged pipeline for training and evaluating a model for a solar irradiance prediction task, taking into account not only meteorological data but also image data. The dual usage of CNN-LSTM and LSTM architectures allows the model to process and learn from both spatial image data and temporal sequence data.
