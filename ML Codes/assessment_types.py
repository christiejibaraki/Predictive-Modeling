import warnings

warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

% matplotlib
inline

# Import Prophet
from fbprophet import Prophet
import logging

logging.getLogger().setLevel(logging.ERROR)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# --------------------------------------------------------------------
df = pd.read_csv('...')
# --------------------------------------------------------------------
# Linear Regression
X = (df['Time_Code']).values
y = (df['OA']).values
X = X.reshape(-1, 1)
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
reg_all = linear_model.LinearRegression()
reg_all.fit(X_train, y_train)
print('-------------------------------------------')
from sklearn import metrics

print('Root Mean Squared Error-Test:', np.sqrt(metrics.mean_squared_error(y_test, reg_all.predict(X_test))))

mse = metrics.mean_squared_error(y_test, reg_all.predict(X_test))
print('Mean Squared Error-Test:', mse)
# -----------------------------------
# fit final model (Predictions-LR)
from sklearn import linear_model

model = linear_model.LinearRegression()
X = df.Time_Code.values
y = (df.OA).values
X = X.reshape(-1, 1)
model.fit(X, y)
Xnew = []
ynew = model.predict(X)
for i in range(len(Xnew)):
    print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))

# -------------------------------------------------------------------------------------
# ARIMA
from statsmodels.tsa.arima.model import ARIMA
from sklearn import metrics

# split into train and test sets
X = df.OA.values
size = int(len(X) * 0.7)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
# walk-forward validation
for t in range(len(test)):
    model = ARIMA(history, order=(1, 1, 2))
    model_fit = model.fit()
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
rmse = np.sqrt(metrics.mean_squared_error(test, predictions))
print('Test MSE: %.3f' % rmse)


# -------------------------------------
# create a differenced series (Predictions-ARIMA)
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)


# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


# seasonal difference
X = df.Total_Assessment.values
Months_in_year = 12
differenced = difference(X, Months_in_year)
# fit model
model = ARIMA(differenced, order=(1, 1, 1))
model_fit = model.fit()
# multi-step out-of-sample forecast
forecast = model_fit.forecast(steps=5)
# invert the differenced forecast to something usable
history = [x for x in X]
month = 1
for yhat in forecast:
    inverted = inverse_difference(history, yhat, Months_in_year)
    print('month %d: %f' % (month, inverted))
    history.append(inverted)
    month += 1
