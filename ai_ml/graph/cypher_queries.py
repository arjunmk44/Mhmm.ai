"""
Parameterized Cypher query templates for Neo4j knowledge graph upserts and queries.
"""

# Upsert Equipment Node
CYPHER_MERGE_EQUIPMENT = """
MERGE (e:Equipment {tag: $tag})
ON CREATE SET e.name = $name, e.id = $tag, e.created_at = timestamp()
ON MATCH SET e.last_updated = timestamp()
RETURN e
"""

# Upsert Document Node
CYPHER_MERGE_DOCUMENT = """
MERGE (d:Document {id: $id})
ON CREATE SET d.filename = $filename, d.document_type = $document_type, d.created_at = timestamp()
ON MATCH SET d.last_updated = timestamp()
RETURN d
"""

# Upsert Person Node
CYPHER_MERGE_PERSON = """
MERGE (p:Person {name: $name})
ON CREATE SET p.id = $name, p.created_at = timestamp()
RETURN p
"""

# Upsert Incident Node
CYPHER_MERGE_INCIDENT = """
MERGE (i:Incident {id: $id})
ON CREATE SET i.title = $title, i.severity = $severity, i.created_at = timestamp()
RETURN i
"""

# Upsert Generic Entity Node
CYPHER_MERGE_GENERIC = """
MERGE (n:%s {id: $id})
ON CREATE SET n.name = $name, n.created_at = timestamp()
RETURN n
"""

# Upsert Directional Relationship
CYPHER_MERGE_RELATIONSHIP = """
MATCH (source {id: $source_id})
MATCH (target {id: $target_id})
MERGE (source)-[r:%s]->(target)
ON CREATE SET r.created_at = timestamp(), r.doc_id = $doc_id
RETURN r
"""

# Query Neighborhood around equipment/entity
CYPHER_GET_NEIGHBORHOOD = """
MATCH (start {id: $entity_id})
OPTIONAL MATCH (start)-[r]-(neighbor)
RETURN start, r, neighbor
LIMIT 50
"""
