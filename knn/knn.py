import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris


def find_x_min(column, dataset):
    x_min = sys.maxsize
    for elem in range(len(dataset)):
        if dataset[elem][column] < x_min:
            x_min = dataset[elem][column]
    return x_min


def find_x_max(column, dataset):
    x_max = -1
    for elem in range(len(dataset)):
        if dataset[elem][column] > x_max:
            x_max = dataset[elem][column]
    return x_max


def dist(pointA, pointB):
    return np.linalg.norm(pointA - pointB)


def normalise_dataset(dataset):
    normalised_dataset = dataset
    for i in range(4):
        x_min = find_x_min(i, normalised_dataset.data)
        x_max = find_x_max(i, normalised_dataset.data)
        for elem in range(len(normalised_dataset.data)):
            normalised_dataset.data[elem][i] = (normalised_dataset.data[elem][i] - x_min) / (x_max - x_min)
    return normalised_dataset


def normalize_item(item, dataset):
    for i in range(4):
        x_min = find_x_min(i, dataset.data)
        x_max = find_x_max(i, dataset.data)
        item[i] = min((item[i] - x_min) / (x_max - x_min), 1)
    return item


def plot_iris(dataset):
    fig, ax = plt.subplots(3, 4)
    result = []
    # print(dataset.feature_names)
    for i in range(4):
        for j in range(i + 1, 4):
            scatter = ax[i][j].scatter(dataset.data[:, i], dataset.data[:, j], c=dataset.target)
            ax[i][j].set(xlabel=dataset.feature_names[i], ylabel=dataset.feature_names[j])
            ax[i][j].legend(scatter.legend_elements()[0], dataset.target_names, loc="lower right", title="classes")
    plt.show()


def find_optimal_k(train_sample, test_sample):
    best_k = None
    best_accuracy = 0.0

    for k in range(1, 21):
        correct_predictions = 0

        for test_item in test_sample:
            distances = []
            for train_item in train_sample:
                distance = dist(train_item[0], test_item[0])
                distances.append((train_item, distance))
                distances.sort(key=lambda x: x[1])

                neighbors = [elem[0] for elem in distances[:k]]

                class_counts = {}

                for neighbor in neighbors:
                    class_of_neighbor = neighbor[-1]
                    if class_of_neighbor in class_counts:
                        class_counts[class_of_neighbor] += 1
                    else:
                        class_counts[class_of_neighbor] = 1

                predicted_class = max(class_counts, key=class_counts.get)

                if predicted_class == test_item[-1]:
                    correct_predictions += 1

            accuracy = correct_predictions / len(test_sample)

            if accuracy > best_accuracy:
                best_k = k
                best_accuracy = accuracy

    return best_k, best_accuracy


def predict_class(new_item, train_sample, k):
    distances = []

    for train_item in train_sample:
        distance = dist(train_item[0], new_item)
        distances.append((train_item, distance))

    distances.sort(key=lambda x: x[1])

    neighbors = [elem[0] for elem in distances[:k]]

    class_counts = {}
    for neighbor in neighbors:
        class_of_neighbor = neighbor[1]
        class_counts[class_of_neighbor] = class_counts.get(class_of_neighbor, 0) + 1

    predicted_class = max(class_counts, key=class_counts.get)

    return predicted_class


if __name__ == '__main__':
    iris = load_iris()
    plot_iris(iris)

    iris_normalised = normalise_dataset(iris)
    plot_iris(iris_normalised)

    train_sample = []
    test_sample = []
    for i in range(len(iris.data)):
        if i in (45, 46, 47, 48, 49, 95, 96, 97, 98, 99, 145, 146, 147, 148, 149):
            test_sample.append([iris.data[i], iris.target[i]])
        else:
            train_sample.append([iris.data[i], iris.target[i]])
    print(find_optimal_k(train_sample, test_sample))

    new_item = [4.8, 3.7, 1.4, 0.3]
    normalize_item(new_item, load_iris())
    print(new_item)

    predicted_class = predict_class(new_item, train_sample, 21)
    print(iris.target_names[predicted_class])