# Efficient-Query-Processing-on-Distributed-Systems

##  Before you start reading this - make sure to change the branch to Phase-2 
This project demonstrates setting up a scalable data processing pipeline using Minikube, Kafka, and Neo4j.

---

## Step 1: **Setting up Minikube and Kafka**

### **1. Install Minikube**

- Install Minikube on your local machine if not already installed.
- Start Minikube with adequate resources:
  ```bash
  minikube start --cpus=4 --memory=6000
  ```
- Verify the installation by setting up Zookeeper and Kafka:
  ```bash
  kubectl apply -f ./zookeeper-setup.yaml
  kubectl apply -f ./kafka-setup.yaml
  ```

### **2. Deploy Neo4j**

- Install Neo4j using Helm and apply service configuration:
  ```bash
  helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml
  kubectl apply -f neo4j-service.yaml
  ```

### **3. Set up Kafka to Neo4j Connector**

- Deploy the Kafka-Neo4j connector to stream data:
  ```bash
  kubectl apply -f kafka-neo4j-connector.yaml
  ```

---

## Step 2: **Check Pod and Service Status**

- Verify that all services and pods are running:
  ```bash
  kubectl get pods
  ```

---

## Step 3: **Port Forwarding**

- Forward the Neo4j and Kafka ports for external access:
  ```bash
  kubectl port-forward svc/neo4j-service 7474:7474 7687:7687
  kubectl port-forward svc/kafka-service 9092:9092
  ```

---

## Step 4: **Run Data Pipeline**

- Produce and test data through the pipeline:
  ```bash
  python3 data_producer.py
    ```
    ```bash
    Message sent to Kafka: b'{"trip_distance":2.13,"PULocationID":169,"DOLocationID":247,"fare_amount":10.47}'
    Message sent to Kafka: b'{"trip_distance":0.92,"PULocationID":81,"DOLocationID":259,"fare_amount":8.8}'
    Message sent to Kafka: b'{"trip_distance":12.5,"PULocationID":51,"DOLocationID":159,"fare_amount":41.23}'
    Message sent to Kafka: b'{"trip_distance":4.62,"PULocationID":20,"DOLocationID":247,"fare_amount":18.7}'
    Message sent to Kafka: b'{"trip_distance":8.74,"PULocationID":169,"DOLocationID":51,"fare_amount":29.36}'
    Message sent to Kafka: b'{"trip_distance":1.09,"PULocationID":250,"DOLocationID":250,"fare_amount":8.8}'
    Message sent to Kafka: b'{"trip_distance":1.84,"PULocationID":78,"DOLocationID":242,"fare_amount":10.66}'
      ```


  
 ```bash
  python3 tester.py
```
```bash
venvkuntal@MacBookPro kt_p1p2 % python3 tester.py                                             
Trying to connect to server 
Server is running

----------------------------------
Testing if data is loaded into the database
1530
42
        Count of Nodes is correct: PASS
        Count of Edges is correct: PASS
Testing if PageRank is working
({'name': 159, 'score': 3.228248647841576}, {'name': 59, 'score': 0.18247321163950955})
        PageRank Test 1: PASS
Testing if BFS is working
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function: `id`.} {position: line: 3, column: 18, offset: 83} for query: "\n            MATCH (a:Location{name:159}), (d:Location{name:212})\n            WITH id(a) AS source, [id(d)] AS targetNodes\n            CALL gds.bfs.stream('TripGraph', {\n            sourceNode: source,\n            targetNodes: targetNodes\n            })\n            YIELD path\n            RETURN path\n        "
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function: `id`.} {position: line: 3, column: 36, offset: 101} for query: "\n            MATCH (a:Location{name:159}), (d:Location{name:212})\n            WITH id(a) AS source, [id(d)] AS targetNodes\n            CALL gds.bfs.stream('TripGraph', {\n            sourceNode: source,\n            targetNodes: targetNodes\n            })\n            YIELD path\n            RETURN path\n        "
        BFS Test 2: PASS
----------------------------------

Testing Complete: Note that the test cases are not exhaustive. You should run your own tests to ensure that your code is working correctly.
venvkuntal@MacBookPro kt_p1p2 %
 ```
---

## Optional: Restart Neo4j

- Restart the Neo4j pod if needed:
  ```bash
  kubectl delete pod pod_name
  ```

---

### **Notes:**

- Ensure that all YAML files are correctly configured.
- Verify network connections if any service is inaccessible.
