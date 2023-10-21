import math
import sys
import copy

import numpy as np
import matplotlib.pyplot as plt
import random


class Point:
    def __init__(self, x, y, centroid=None, cluster=None):
        self.x = x
        self.y = y
        self.centroid = centroid
        self.cluster = cluster


def random_points(n):
    points = []
    for i in range(n):
        points.append(Point(random.randint(0, 100), random.randint(0, 100)))
    return points


def dist(pointA, pointB):
    return math.sqrt((pointA.x - pointB.x) ** 2 + (pointA.y - pointB.y) ** 2)


def first_centroids(points, n):
    point_center = Point(0, 0)
    for elem in points:
        point_center.x += elem.x
        point_center.y += elem.y
    point_center.x /= len(points)
    point_center.y /= len(points)

    R = 0
    for elem in points:
        distCurr = dist(elem, point_center)
        if distCurr > R:
            R = distCurr
    centroids = []

    for i in range(n):
        centroid = Point(R * np.cos(2 * np.pi * i / n) + point_center.x,
                         R * np.sin(2 * np.pi * i / n) + point_center.y)
        centroids.append(centroid)

    return centroids


def show_points(points):
    colors = ['b', 'g', 'c', 'm', 'y', 'k', 'orange', 'yellowgreen', 'pink']

    clusters = {}
    for point in points:
        cluster = point.centroid
        if cluster in clusters:
            clusters[cluster].append(point)
        else:
            clusters[cluster] = [point]

    for i, (cluster, color) in enumerate(zip(clusters.values(), colors)):
        x = [point.x for point in cluster]
        y = [point.y for point in cluster]
        plt.scatter(x, y, color=color)


def show_first_step():
    show_points(points)
    for i in range(n):
        plt.scatter(centroids[i].x, centroids[i].y, marker='s', color="r")

    plt.savefig("1.png")
    plt.show()


def k_means(points, centroids, finding_optimal):
    threshold = 1e-5
    iteration = 2
    one_more = True

    while one_more:
        prev_centroids = copy.deepcopy(centroids)

        for point in points:
            min_dist = sys.maxsize
            point.cluster = None
            for centroid in centroids:
                if dist(point, centroid) < min_dist:
                    min_dist = dist(point, centroid)
                    point.centroid = centroid
                    point.cluster = centroids.index(centroid)

        for centroid in centroids:
            centroid_points = []
            for point in points:
                if point.centroid == centroid:
                    centroid_points.append(point)
            update_centroid(centroid_points, centroid, finding_optimal)

        if not finding_optimal:
            show_points(points)
            plt.savefig(str(iteration) + ".png")
            plt.show()
            iteration += 1

        one_more = any(dist(prev, curr) > threshold for prev, curr in zip(prev_centroids, centroids))

    return points, centroids


def update_centroid(centroid_points, centroid, finding_optimal):
    avg_x = 0
    avg_y = 0
    for centroid_point in centroid_points:
        avg_x += centroid_point.x
        avg_y += centroid_point.y
    avg_x /= len(centroid_points)
    avg_y /= len(centroid_points)

    centroid.x = avg_x
    centroid.y = avg_y
    if not finding_optimal:
        plt.scatter(centroid.x, centroid.y, marker='s', c='r')


def find_optimal_clusters(points):
    criteria = []
    iterations = math.sqrt(len(points))

    for i in range(int(iterations)):
        temp_points = points
        centroids = first_centroids(temp_points, i + 1)
        temp_points, centroids = k_means(temp_points, centroids, True)
        criteria.append(sum(dist(point, centroids[point.cluster]) ** 2 for point in temp_points))

    # разница между двумя суммами
    diff = np.diff(criteria)

    # масштаб изменений между кластерами
    diff_cluster = diff[1:] / diff[:-1]

    plt.plot(diff_cluster)
    plt.savefig("scale_of_changes")
    min = sys.maxsize
    cluster = 0

    for p in points:
        p.centroid = None

    for i in range(len(diff_cluster)):
        if min > diff_cluster[i] and diff_cluster[i] > 0:
            min = diff_cluster[i]
            cluster = i + 2
    return cluster


if __name__ == "__main__":
    points = random_points(100)
    n = find_optimal_clusters(points)
    print(str(n) +" кластеров")
    centroids = first_centroids(points, n)
    show_first_step()
    k_means(points, centroids, finding_optimal=False)

