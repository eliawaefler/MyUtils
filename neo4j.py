from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def write_data(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.write_transaction(self._execute_write_query, query, parameters)
            return result

    def read_data(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.read_transaction(self._execute_read_query, query, parameters)
            return result

    @staticmethod
    def _execute_write_query(tx, query, parameters):
        result = tx.run(query, parameters)
        return result.consume()

    @staticmethod
    def _execute_read_query(tx, query, parameters):
        result = tx.run(query, parameters)
        return [record.data() for record in result]

# Usage example
if __name__ == "__main__":
    # Connect to the database
    uri = os.environ["neo4j_url1"]
    user = "neo4j"
    password = os.environ["NEO4J_PW1"]

    neo4j_handler = Neo4jHandler(uri, user, password)

    # Write data
    create_query = """
    CREATE (p:Person {name: $name, age: $age})
    RETURN p
    """
    parameters = {"name": "Alice", "age": 30}
    write_result = neo4j_handler.write_data(create_query, parameters)
    print("Write result:", write_result)

    # Read data
    read_query = """
    MATCH (p:Person)
    RETURN p.name AS name, p.age AS age
    """
    read_result = neo4j_handler.read_data(read_query)
    print("Read result:", read_result)

    # Close the connection
    neo4j_handler.close()
