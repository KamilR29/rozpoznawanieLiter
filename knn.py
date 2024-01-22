import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def load_data(file_name):
    data = np.loadtxt(file_name, delimiter=',', dtype=str)
    labels = data[:, 0]
    features = data[:, 1:].astype(float)
    return features, labels

def knn_sklearn(train_file, test_file, k):
    # Load training and testing data
    train_features, train_labels = load_data(train_file)
    test_features, test_labels = load_data(test_file)

    # Initialize the kNN classifier
    knn_classifier = KNeighborsClassifier(n_neighbors=k)

    # Train the classifier
    knn_classifier.fit(train_features, train_labels)

    # Predict labels for the test set
    predictions = knn_classifier.predict(test_features)

    # Calculate accuracy
    accuracy = accuracy_score(test_labels, predictions)
    return accuracy