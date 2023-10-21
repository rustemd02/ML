import math
import random
import pygame


class Point:
    def __init__(self, x, y, isVisited=None, isNoise=None, isBorder=None, isPartOfCluster=None, flag=None, cluster_color=None):
        self.isPartOfCluster = isPartOfCluster
        self.isVisited = isVisited
        self.isNoise = isNoise
        self.isBorder = isBorder
        self.cluster_color = cluster_color
        self.flag = flag
        self.x = x
        self.y = y


def dbscan(points):
    clusters = []

    for point in points:
        if point.isVisited:
            continue
        else:
            point.isVisited = True
            neighbours = find_neighbours(point, points)
            if len(neighbours) == 0:
                point.isNoise = True
            elif len(neighbours) >= 4:
                point.cluster_color = colors[len(clusters)]
                cluster = expand_cluster(point, neighbours, clusters)
                clusters.append(cluster)
    return clusters


def expand_cluster(point, neighbours, clusters):
    cluster = [point]
    for neighbour in neighbours:
        if not neighbour.isVisited:
            neighbour.isVisited = True
            sub_neighbours = find_neighbours(neighbour, neighbours)
            if len(sub_neighbours) >= 4:
                neighbours.extend(sub_neighbours)
            else:
                point.isBorder = True
        if not neighbour.isPartOfCluster:
            cluster.append(neighbour)
            neighbour.cluster_color = colors[len(clusters)]
            neighbour.isPartOfCluster = True
    return cluster


def find_neighbours(point, points):
    neighbours = []
    for neighbour in points:
        if point != neighbour and dist(neighbour, point) <= 25:
            neighbours.append(neighbour)
    return neighbours


def dist(pointA, pointB):
    return math.sqrt((pointA.x - pointB.x) ** 2 + (pointA.y - pointB.y) ** 2)


if __name__ == '__main__':
    colors = ["#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#800080", "#FFD700", "#008080", "#FF1493", "#FFA500"]

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill(color="#FFFFFF")
    pygame.display.update()
    points = []
    flag = True
    is_up = False

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_up = True
                if event.button == 1:
                    is_up = True
            if event.type == pygame.MOUSEBUTTONUP:
                is_up = False
            if is_up:
                coord = event.pos
                if random.randint(0, 2) == 2:
                    points.append(Point(coord[0], coord[1]))
                    pygame.draw.circle(screen, color='black', center=coord, radius=3)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dbscan(points)
                    for point in points:
                        if point.isNoise:
                            pygame.draw.circle(screen, color='red', center=(point.x, point.y), radius=3)
                        elif point.isBorder:
                            pygame.draw.circle(screen, color='yellow', center=(point.x, point.y), radius=3)
                            pygame.draw.circle(screen, color="black", center=(point.x, point.y), radius=30, width=1)
                        else:
                            pygame.draw.circle(screen, color='green', center=(point.x, point.y), radius=3)
                if event.key == pygame.K_SPACE:
                    screen.fill(color="#FFFFFF")
                    clusters = dbscan(points)
                    for point in points:
                        if point.isNoise:
                            pygame.draw.circle(screen, color='red', center=(point.x, point.y), radius=3)
                        else:
                            if point.cluster_color is not None:
                                pygame.draw.circle(screen, color=point.cluster_color, center=(point.x, point.y), radius=3)
        pygame.display.update()
    pygame.quit()
