# Solar Irradiance Prediction using Deep Neural Network.
[![Python 3.10](https://img.shields.io/badge/Python-3.10-orange)](https://www.python.org/downloads/release/python-3102/)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen)](https://github.com/marianSTU/solar-irradiance-prediction/blob/main/LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.11.1-brightgreen)](https://www.tensorflow.org/api_docs)
[![Keras](https://img.shields.io/badge/Keras-API-green)](https://keras.io/guides/functional_api/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5.3-red)](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)
[![SkyCam](https://img.shields.io/badge/Dataset-SkyCam-blueviolet)](https://github.com/vglsd/SkyCam)
[![Author](https://img.shields.io/badge/Author-Bc.Marián_Šebeňa-blue)](https://is.stuba.sk/lide/clovek.pl?id=97945;)

## Prerequisites:

- Python programming knowledge
- Basic understanding of Machine Learning and Neural Networks
- TensorFlow and Keras installed on your system.

## Data format
 
- Images shape = (64, 64, 5)
- meteorological data shape = (5, 6)

## Steps:

### Step 1: Import necessary libraries

First,  import the necessary libraries. 

```python
import tensorflow as tf
from tensorflow import keras
```

### Step 2: Load the pretrained model

'solar_irradiance_predictor.h5', you can load using the load_model function.

```python
model = keras.models.load_model('solar_irradiance_predictor.h5')
```

### Step 3: Check the model's summary

To verify if the model is loaded correctly, you can print the model's summary.

```python
model.summary()
```

### Step 4: Use the model for predictions
To make predictions, you need to pass the data to the predict method. 
Ensure that your data is in the correct format explained above.

```python
predictions = model.predict([images, met_data])
```