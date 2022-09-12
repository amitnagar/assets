# Examples of how various transformation can be done to data using sklearn preprocessing class
#
# The sklearn.preprocessing package provides several common utility functions & transformer
# classes to change raw feature vectors into a representation that is more suitable for the
# downstream estimators.

from sklearn import preprocessing
import numpy as np

X = np.array([[1, 2], [100, 2], [1, 3]])

# Scaling the data
scaler = preprocessing.StandardScaler().fit(X)
scaled_data = scaler.transform(X)

print(scaled_data)

# instead of using fit and then transform, we use fit_transform
scaled_data = scaler.fit_transform(X)

print(scaled_data)

# Minmax scaler
minmax = preprocessing.MinMaxScaler()
minmax_fit = minmax.fit(X)
minmax_scaled = minmax_fit.transform(X)

print(minmax_scaled)

# use fit_transform directly
minmax = preprocessing.MinMaxScaler()
minmax_scaled = minmax.fit_transform(X)

print(minmax_scaled)
