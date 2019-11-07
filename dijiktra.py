# Problem: Given a map of the cities and their bidirectional roads, determine which roads are along any shortest path. Write a classifyEdges function which must return an array of g_edges strings where the value at ith index is YES if the ith edge is a part of a shortest path from vertex 1 to vertex g_nodes. Otherwise it should contain NO.

from collections import OrderedDict

def getGraphAndPaths(g_from, g_to, g_weight):
    map, valid_paths = {}, OrderedDict()
    
    for i in range(len(g_from)):
        s = min(g_from[i], g_to[i])
        d = max(g_from[i], g_to[i])
        valid_paths[(s, d)] = 0
        
        if s not in map:
            map[s] = []
        map[s].append([d, g_weight[i]])
        
    return map, valid_paths

def shortestPath(map, g_nodes):
    nodes_min_dist = {}
    return shortestPathHelper(map, 1, g_nodes, nodes_min_dist)

def shortestPathHelper(map, source, dest, nodes_min_dist):
    if source in nodes_min_dist:
        return nodes_min_dist[source]

    min_weight = float('inf')
    for node, weight in map[source]:
        if node == dest:
            if weight < min_weight:
                min_weight = weight
        else:
            path_weight = weight + shortestPathHelper(map, node, dest, nodes_min_dist)
            if path_weight < min_weight:
                min_weight = path_weight

    nodes_min_dist[source] = min_weight
    return min_weight

def getPaths(dest, min_path, map, valid_paths):
    getPathsHelper(1, 0, dest, min_path, map, valid_paths)
    
def getPathsHelper(source, path_wt_so_for, dest, min_path, map, valid_paths):
    if source == dest:
        return True
    
    isPath = False
    for node, wt in map[source]:
        if path_wt_so_for + wt <= min_path:
            isPath = getPathsHelper(node, path_wt_so_for + wt, dest, min_path, map, valid_paths)
            if isPath:
                if (source,node) in valid_paths:
                    valid_paths[(source, node)] += 1
                else:
                    valid_paths[(dest, source)] += 1
    return isPath


def classifyEdges(g_nodes, g_from, g_to, g_weight):
    map, valid_paths = getGraphAndPaths(g_from, g_to, g_weight)

    min_path = shortestPath(map, g_nodes)

    getPaths(g_nodes, min_path, map, valid_paths)
    
    output = []
    for edge in valid_paths:
        if valid_paths[edge] != 0:
            output.append("YES")
        else:
            output.append("NO")
    return output


g_nodes = 5
g_from = [1,2,3,1,4,3,2]
g_to = [2,3,5,4,5,4,4] 
g_weight = [1,1,1,1,2,2,4]
print(classifyEdges(g_nodes, g_from, g_to, g_weight))
        