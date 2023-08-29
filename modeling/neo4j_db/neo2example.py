from py2neo import Graph, Node, Relationship, NodeMatcher
from pandas import DataFrame
import os
import pandas as pd
import csv
from collections import defaultdict

# graph = py2neo.Graph('http://localhost:7474', auth=('neo4j', 'root'))
graph = Graph("http://localhost:7474", user="neo4j", password="neo4j1")
matcher = NodeMatcher(graph)


ner_file = "../data/submission_ner_rel.csv"
paper_file = "../data/submission_paper_rel.csv"

# Create ner node
if not os.path.exists(ner_file):
    print('{} Non-existed'.format(ner_file))
df = pd.read_csv(ner_file, header=0, encoding='utf-8',quoting=csv.QUOTE_ALL, error_bad_lines=False)
df = df.fillna(value=str('Non-existed'))

df['id_src'] = df[['index','source']].to_dict('records')
df['id_tar'] = df[['index', 'target']].to_dict('records')

node_dict_list = []
for i in df['id_src']:
    node_dict= {}
    node_dict["id"] = i['source']
    if len(str(i['source'])) > 10:
        node_dict["name"] = str(i['source'])[:10] + "..."
    else:
        node_dict["name"] = i['source']
    node_dict["label"] = i['index']
    node_dict_list.append(node_dict)

for i in df['id_tar']:
    node_dict= {}
    node_dict["id"] = i['target']
    if len(str(i['target'])) > 10:
        node_dict["name"] = str(i['target'])[:10] + "..."
    else:
        node_dict["name"] = i['target']
    node_dict["label"] = i['index']
    node_dict_list.append(node_dict)

df1 = pd.DataFrame(node_dict_list)
df1 = df1.drop_duplicates(subset=['id'])
print(df1)

a =df1['id']
b =df1['name']
c =df1['label']
for data in zip(a,b,c):
    node = Node('NER_Bio', name=data[1])
    node['id']=data[0]
    node['name']=data[1]
    node['Source']=data[2]
    graph.create(node)


# Create paper node
paper_dict_list = []
if not os.path.exists(paper_file):
    print('{} Non-existed'.format(paper_file))
df = pd.read_csv(paper_file, header=0, encoding='utf-8',quoting=csv.QUOTE_ALL, error_bad_lines=False)
df = df.fillna(value=str('Non-existed'))

df['id_src'] = df[['index','source']].to_dict('records')
df['id_tar'] = df[['index', 'target']].to_dict('records')

node_dict_list = []
for i in df['id_src']:
    node_dict= {}
    node_dict["id"] = i['source']
    node_dict["name"] = i['source']
    node_dict["label"] = i['index']
    node_dict_list.append(node_dict)

for i in df['id_tar']:
    node_dict= {}
    node_dict["id"] = i['target']
    node_dict["name"] = i['target']
    node_dict["label"] = i['index']
    node_dict_list.append(node_dict)

df1 = pd.DataFrame(node_dict_list)
df1 = df1.drop_duplicates(subset=['id'])
print(df1)

a =df1['id']
b =df1['name']
c =df1['label']
for data in zip(a,b,c):
    node = Node('Paper', name=data[1])
    node['id']=data[0]
    node['name']=data[1]
    node['Source']=data[2]
    graph.create(node)


# Relation Q2Q
print("Relation Q2Q")
if not os.path.exists(ner_file):
    print('{} Non-existed'.format(ner_file))
df = pd.read_csv(ner_file, header=0, encoding='utf-8',quoting=csv.QUOTE_ALL, error_bad_lines=False)
df = df.fillna(value=str('Non-existed'))
col=df.columns
for data in zip(df[col[0]], df[col[1]], df[col[2]], df[col[3]]):
    from_node=matcher.match("NER_Bio", id=data[1]).first()
    to_id=matcher.match("NER_Bio",id=data[3]).first()

    #paper={"paper_uid:":str(data[0])}
    #Relationship(from_node, data[2], to_id,**paper)

    graph.create(Relationship(from_node, data[2], to_id))


# Relation Q2P
print("Relation Q2P")
if not os.path.exists(ner_file):
    print('{} Non-existed'.format(ner_file))
df = pd.read_csv(ner_file, header=0, encoding='utf-8',quoting=csv.QUOTE_ALL, error_bad_lines=False)
df = df.fillna(value=str('Non-existed'))

col=df.columns
for data in zip(df[col[0]], df[col[1]], df[col[2]], df[col[3]]):
    from_node=matcher.match("Paper", id=data[0]).first()
    to_id=matcher.match("NER_Bio",id=data[1]).first()

    #paper={"paper_uid:":str(data[0])}
    #Relationship(from_node, data[2], to_id,**paper)

    graph.create(Relationship(from_node, "with keyword", to_id))


# Relation P2P
print("Relation P2P")
if not os.path.exists(paper_file):
    print('{} Non-existed'.format(paper_file))
df = pd.read_csv(paper_file, header=0, encoding='utf-8',quoting=csv.QUOTE_ALL, error_bad_lines=False)
df = df.fillna(value=str('Non-existed'))

col=df.columns
for data in zip(df[col[0]], df[col[1]], df[col[2]], df[col[3]]):
    from_node=matcher.match("Paper", id=data[1]).first()
    to_id=matcher.match("Paper",id=data[3]).first()

    graph.create(Relationship(from_node, data[2], to_id))


