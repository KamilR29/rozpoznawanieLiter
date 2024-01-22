import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def load_data(file_name):
    data = np.loadtxt(file_name, delimiter=',', dtype=str)
    labels = data[:, 0]
    features = data[:, 1:].astype(float)
    return features, labels

def naive_bayes_sklearn(train_file, test_file):
    # Load training and testing data
    train_features, train_labels = load_data(train_file)
    test_features, test_labels = load_data(test_file)

    # Initialize the Naive Bayes classifier
    nb_classifier = GaussianNB()

    # Train the classifier
    nb_classifier.fit(train_features, train_labels)

    # Predict labels for the test set
    predictions = nb_classifier.predict(test_features)

    # Calculate accuracy
    accuracy = accuracy_score(test_labels, predictions)
    return accuracy