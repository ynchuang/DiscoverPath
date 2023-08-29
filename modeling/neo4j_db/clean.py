from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph("http://localhost:7474", user="neo4j", password="neo4j1")
graph.run(cypher="Match(n) detach delete n")
