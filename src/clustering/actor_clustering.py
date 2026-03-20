# -*- coding:utf-8 -*-

from core.math import Vector2
import math


class ActorClustering:
    """
    Actor聚类分析类
    使用DBSCAN算法对Actor进行聚类，并选择每个聚类的leader
    """
    
    def __init__(self, eps=50, min_samples=3):
        """
        初始化聚类参数
        
        Args:
            eps: 邻域半径
            min_samples: 形成簇的最小样本数
        """
        self.eps = eps
        self.min_samples = min_samples
    
    def get_actor_features(self, actor):
        """
        提取Actor的特征数据
        
        Args:
            actor: Actor实例
        
        Returns:
            特征向量 (x, y, speed)
        """
        return [actor.actor_pos.x, actor.actor_pos.y, actor.actor_speed]
    
    def distance(self, feature1, feature2):
        """
        计算两个特征向量之间的欧氏距离
        
        Args:
            feature1: 第一个特征向量
            feature2: 第二个特征向量
        
        Returns:
            欧氏距离
        """
        return math.sqrt(
            (feature1[0] - feature2[0]) ** 2 +
            (feature1[1] - feature2[1]) ** 2 +
            (feature1[2] - feature2[2]) ** 2
        )
    
    def get_neighbors(self, actors, features, index):
        """
        获取指定Actor的邻居
        
        Args:
            actors: Actor列表
            features: 特征向量列表
            index: 当前Actor的索引
        
        Returns:
            邻居索引列表
        """
        neighbors = []
        for i, feature in enumerate(features):
            if i != index and self.distance(features[index], feature) <= self.eps:
                neighbors.append(i)
        return neighbors
    
    def dbscan(self, actors):
        """
        使用DBSCAN算法进行聚类（优化版本）
        
        Args:
            actors: Actor列表
        
        Returns:
            聚类结果，每个元素是一个Actor列表
        """
        if not actors:
            return []
        
        # 提取特征
        features = [self.get_actor_features(actor) for actor in actors]
        n = len(actors)
        
        # 初始化聚类标记
        cluster_labels = [-1] * n  # -1表示未分类
        cluster_id = 0
        
        # 预计算距离矩阵，避免重复计算
        distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dist = self.distance(features[i], features[j])
                distance_matrix[i][j] = dist
                distance_matrix[j][i] = dist
        
        def get_neighbors_fast(index):
            """快速获取邻居"""
            neighbors = []
            for i in range(n):
                if i != index and distance_matrix[index][i] <= self.eps:
                    neighbors.append(i)
            return neighbors
        
        for i in range(n):
            # 跳过已分类的点
            if cluster_labels[i] != -1:
                continue
            
            # 获取邻居
            neighbors = get_neighbors_fast(i)
            
            # 检查是否是核心点
            if len(neighbors) < self.min_samples:
                cluster_labels[i] = -2  # 标记为噪声点
                continue
            
            # 扩展簇
            cluster_labels[i] = cluster_id
            queue = neighbors.copy()
            
            while queue:
                j = queue.pop(0)
                if cluster_labels[j] == -1:
                    cluster_labels[j] = cluster_id
                    j_neighbors = get_neighbors_fast(j)
                    if len(j_neighbors) >= self.min_samples:
                        queue.extend(j_neighbors)
                elif cluster_labels[j] == -2:
                    cluster_labels[j] = cluster_id
            
            cluster_id += 1
        
        # 组织聚类结果
        clusters = []
        for cid in range(cluster_id):
            cluster = [actors[i] for i, label in enumerate(cluster_labels) if label == cid]
            clusters.append(cluster)
        
        # 处理噪声点
        noise = [actors[i] for i, label in enumerate(cluster_labels) if label == -2]
        if noise:
            clusters.append(noise)  # 将噪声点作为一个单独的簇
        
        return clusters
    
    def select_leader(self, cluster):
        """
        从聚类中选择leader
        选择标准：
        1. 速度最快的Actor
        2. 如果速度相同，选择位置在聚类中心的Actor
        
        Args:
            cluster: Actor聚类
        
        Returns:
            选择的leader
        """
        if not cluster:
            return None
        
        # 计算聚类中心
        center = Vector2(0, 0)
        for actor in cluster:
            center += actor.actor_pos
        center /= len(cluster)
        
        # 选择速度最快的Actor
        fastest_actors = []
        max_speed = -1
        
        for actor in cluster:
            if actor.actor_speed > max_speed:
                max_speed = actor.actor_speed
                fastest_actors = [actor]
            elif actor.actor_speed == max_speed:
                fastest_actors.append(actor)
        
        # 如果只有一个速度最快的Actor，直接选择
        if len(fastest_actors) == 1:
            return fastest_actors[0]
        
        # 否则选择离中心最近的Actor
        closest_actor = None
        min_distance = float('inf')
        
        for actor in fastest_actors:
            distance = (actor.actor_pos - center).length()
            if distance < min_distance:
                min_distance = distance
                closest_actor = actor
        
        return closest_actor
    
    def silhouette_score(self, actors):
        """
        计算轮廓系数评估聚类质量
        
        Args:
            actors: Actor列表
        
        Returns:
            轮廓系数
        """
        if len(actors) < 2:
            return 0
        
        features = [self.get_actor_features(actor) for actor in actors]
        clusters = self.dbscan(actors)
        
        if len(clusters) == 1:
            return 0
        
        silhouette_scores = []
        
        for i, actor in enumerate(actors):
            # 找到当前Actor所在的簇
            current_cluster = None
            for cluster in clusters:
                if actor in cluster:
                    current_cluster = cluster
                    break
            
            if not current_cluster or len(current_cluster) == 1:
                continue
            
            # 计算簇内平均距离
            a = 0
            for other_actor in current_cluster:
                if other_actor != actor:
                    a += self.distance(
                        self.get_actor_features(actor),
                        self.get_actor_features(other_actor)
                    )
            a /= (len(current_cluster) - 1)
            
            # 计算到其他簇的最小平均距离
            b = float('inf')
            for cluster in clusters:
                if cluster != current_cluster and cluster:
                    cluster_distance = 0
                    for other_actor in cluster:
                        cluster_distance += self.distance(
                            self.get_actor_features(actor),
                            self.get_actor_features(other_actor)
                        )
                    cluster_distance /= len(cluster)
                    if cluster_distance < b:
                        b = cluster_distance
            
            # 计算轮廓系数
            if max(a, b) > 0:
                s = (b - a) / max(a, b)
                silhouette_scores.append(s)
        
        return sum(silhouette_scores) / len(silhouette_scores) if silhouette_scores else 0
    
    def cluster_and_select_leaders(self, actors):
        """
        执行聚类分析并选择每个聚类的leader
        
        Args:
            actors: Actor列表
        
        Returns:
            (clusters, leaders, silhouette_score)
            clusters: 聚类结果
            leaders: 每个聚类的leader
            silhouette_score: 聚类质量评估指标
        """
        # 执行聚类
        clusters = self.dbscan(actors)
        
        # 选择每个聚类的leader
        leaders = [self.select_leader(cluster) for cluster in clusters]
        
        # 计算轮廓系数
        score = self.silhouette_score(actors)
        
        return clusters, leaders, score
