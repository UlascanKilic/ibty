visited = []

def dfs(graph, node):
    global visited
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n)

def dfs_search(graph, node):
    global visited
    visited = []
    dfs(graph, node)
    return visited
