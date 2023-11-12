import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC


class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color


def random_points(n):
    point_samples = []
    point_features = []
    for i in range(n):
        point_samples.append(Point(random.randint(0, 50), random.randint(0, 50), "red"))
    for i in range(n):
        point_features.append(Point(random.randint(60, 100), random.randint(60, 100), "blue"))
    return point_samples, point_features


def optimal_line(point_samples, point_features):
    clf = svc(point_features, point_samples)

    for point in point_samples:
        plt.scatter(point.x, point.y, c='red')
    for point in point_features:
        plt.scatter(point.x, point.y, c='blue')

    # отвечают за получение текущих пределов осей x и y на текущем графике
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()

    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 50), np.linspace(ylim[0], ylim[1], 50))
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, colors='k', levels=[0], alpha=0.5, linestyles=['-'])

    plt.show()


def svc(point_features, point_samples):
    # Преобразование в массивы NumPy
    X = np.array([[point.x, point.y] for point in point_samples + point_features])
    y = np.array([0] * len(point_samples) + [1] * len(point_features))
    # Обучение SVM
    clf = SVC(kernel='linear')
    clf.fit(X, y)
    return clf


if __name__ == '__main__':
    n = 50
    point_samples, point_features = random_points(n)
    for i in range(n):
        plt.scatter(point_samples[i].x, point_samples[i].y, c=point_samples[i].color)
        plt.scatter(point_features[i].x, point_features[i].y, c=point_features[i].color)
    plt.show()

    optimal_line(point_samples, point_features)

    new_point = [random.randint(0, 100), random.randint(0, 100)]
    class_prediction = svc(point_features, point_samples).predict([new_point])
    if class_prediction == 0:
        plt.scatter(new_point[0], new_point[1], c='lightcoral')
    else:
        plt.scatter(new_point[0], new_point[1], c='cyan')

    optimal_line(point_samples, point_features)
    plt.show()
