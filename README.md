# DiscoverPath: A Knowledge Refinement and Retrieval System for Interdisciplinarity on Biomedical Research
<img width="300" height="200" src="./fig/logo.png">

## About this project

This project focus on interdisciplinary knowledge exploration in biomedical research. To increase the convenience of exploration, we build [DiscoverPath](https://www.researchgate.net/publication/369755614_DiscoverPath_A_Knowledge_Refinement_and_Retrieval_System_for_Interdisciplinarity_on_Biomedical_Research) system, a knowledge graph based retrieval system for interdisciplinary knowledge exploration in biomedical research. Biomedical research can significantly benefit from a powerful information retrieval system. However, existing tools heuristically adopt surface elements to represent an entity for retrieval, such as the authors and terminologies of an article, which severely limits the discovery of interdisciplinary knowledge hidden from different entities.

<div align=center>
<img width="500" height="300" src="./fig/KG1.png">
</div>

## Utilization and Demonstration of DiscoverPath

### Interface
The overall GUI interface of the DiscoverPath system, which consists of a frontend interaction, a backend platform, and a graph database.

<div align=center>
<img width="650" height="350" src="./fig/demo.png">
</div>


### Utilization
A using pipeline overview of DiscoverPath based on a client-server architecture. DiscoverPath follows a pipeline to gradually refine the knowledge graphs that meet the requirements of users. Users first give their initial queries to get the initial knowledge graphs, and then utilize the recommended queries to refine the initial one before visualizing the Interdisciplinary knowledge.

<div align=center>
<img width="500" height="300" src="./fig/pipeline.png">
</div>

### Demonstration
DiscoverPath system shows the results of interdisciplinary knowledge exploration. We here select serveral results in Alzheimer’s disease, which is shown as follows:

<div align=center>
<img width="500" height="400" src="./fig/eval.png">
</div>


##  Install Environment
```sh
-  OpenJDK 1.8
-  Python 3.7
-  neo4j 3.5
```

### start neo4j server
```sh
<NEO4J_HOME>/bin/neo4j console
<NEO4J_HOME>/bin/neo4j start
./bin/neo4j-admin  set-initial-password neo4j1
```

### Initiaize Neo4j Data
```sh
python clean.py
python neo2example.py
```

## Cite this work

If you find this project useful, you can cite this work by:
````angular2html
@article{chuang2018discoverpath,
  title={DiscoverPath: A Knowledge Refinement and Retrieval System for Interdisciplinarity on Biomedical Research},
  author={Chuang, Yu-Neng and Wang, Guanchu and Chang, Chia-Yuan and Lai, Kwei-Herng and Zha, Daochen and Tang, Ruixiang and Yang, Fan and Reyes, Alfredo Costilla and Zhou, Kaixiong and Jiang, Xiaoqian and Hu, Xia},
  year={2023}
}
````
