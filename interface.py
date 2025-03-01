from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "project2phase2"

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def createProjection(self):
        query = """CALL gds.graph.project(
                    'TripGraph',
                    'Location',
                    'TRIP',
                    {
                        relationshipProperties: 'distance'
                    }
                    )
                    """
        with self._driver.session() as session:
            session.run(query)

    def deleteProjection(self):
        query = """CALL gds.graph.drop('TripGraph') YIELD graphName;"""
        with self._driver.session() as session:
            session.run(query)

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        # raise NotImplementedError
        self.createProjection()

        query = """
            MATCH (a:Location{name:%(start_node)s}), (d:Location{name:%(last_node)s})
            WITH id(a) AS source, [id(d)] AS targetNodes
            CALL gds.bfs.stream('TripGraph', {
            sourceNode: source,
            targetNodes: targetNodes
            })
            YIELD path
            RETURN path
        """% {'start_node': start_node, 'last_node': last_node}
        
        with self._driver.session() as session:
            result = session.run(query)
            records = result.data()

        self.deleteProjection()
        
        return records

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        # raise NotImplementedError

        self.createProjection()

        query = """
            CALL gds.pageRank.stream('TripGraph', {
            maxIterations: %(max_iterations)s,
            dampingFactor: 0.85,
            relationshipWeightProperty: '%(weight_property)s'
            })
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).name AS name, score
            ORDER BY score DESC, name ASC
        """% {'max_iterations': max_iterations, 'weight_property': weight_property}

        records = None
        with self._driver.session() as session:
            result = session.run(query)
            records = result.data()

        self.deleteProjection()

        if records:
            max_score_node = records[0]
            min_score_node = records[-1]
            return max_score_node, min_score_node
        else:
            return None, None