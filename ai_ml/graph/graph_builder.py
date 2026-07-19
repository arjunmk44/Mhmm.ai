"""
Graph Builder module for persisting extracted entities and relationships into Neo4j / NetworkX memory graph.
"""

from typing import Dict, Any, List
from ai_ml.graph.neo4j_client import neo4j_client
from ai_ml.graph.entity_resolution import entity_resolver
from ai_ml.graph.cypher_queries import (
    CYPHER_MERGE_EQUIPMENT,
    CYPHER_MERGE_DOCUMENT,
    CYPHER_MERGE_PERSON,
    CYPHER_MERGE_GENERIC,
)
from ai_ml.utils.logger import logger


class GraphBuilder:

    def build_graph(self, document_id: str, filename: str, extraction_data: Dict[str, Any]) -> int:
        """
        Processes extraction output, performs entity resolution, and merges nodes and edges into graph.
        Returns total count of graph elements created/updated.
        """
        elements_count = 0
        doc_type = extraction_data.get("document_type", "project_file")
        entities = extraction_data.get("entities", {})
        relationships = extraction_data.get("relationships", [])

        # 1. Merge Document Node
        neo4j_client.run_query(CYPHER_MERGE_DOCUMENT, {
            "id": document_id,
            "filename": filename,
            "document_type": doc_type
        })
        if neo4j_client.memory_graph is not None:
            neo4j_client.memory_graph.add_node(document_id, label="Document", properties={"filename": filename, "type": doc_type})
        elements_count += 1

        # 2. Merge Equipment Nodes & create MENTIONED_IN edges
        raw_eq_tags = entities.get("equipment_tags", [])
        resolved_tags = entity_resolver.deduplicate_tags(raw_eq_tags)

        for tag in resolved_tags:
            neo4j_client.run_query(CYPHER_MERGE_EQUIPMENT, {"tag": tag, "name": tag})
            rel_query = f"MATCH (e:Equipment {{tag: $tag}}), (d:Document {{id: $doc_id}}) MERGE (e)-[r:MENTIONED_IN]->(d) RETURN r"
            neo4j_client.run_query(rel_query, {"tag": tag, "doc_id": document_id})

            if neo4j_client.memory_graph is not None:
                neo4j_client.memory_graph.add_node(tag, label="Equipment", properties={"name": tag})
                neo4j_client.memory_graph.add_edge(tag, document_id, type="MENTIONED_IN")
            elements_count += 2

        # 3. Merge Personnel
        personnel = entities.get("personnel", [])
        for person in personnel:
            neo4j_client.run_query(CYPHER_MERGE_PERSON, {"name": person})
            rel_query = f"MATCH (p:Person {{name: $person}}), (d:Document {{id: $doc_id}}) MERGE (p)-[r:MENTIONED_IN]->(d) RETURN r"
            neo4j_client.run_query(rel_query, {"person": person, "doc_id": document_id})

            if neo4j_client.memory_graph is not None:
                neo4j_client.memory_graph.add_node(person, label="Person", properties={"name": person})
                neo4j_client.memory_graph.add_edge(person, document_id, type="MENTIONED_IN")
            elements_count += 2

        # 4. Merge Relationships
        for rel in relationships:
            src = rel.get("from") or rel.get("source")
            tgt = rel.get("to") or rel.get("target")
            r_type = (rel.get("type") or "CONNECTED_TO").upper()

            if src and tgt:
                res_src = entity_resolver.resolve_tag(src, resolved_tags)
                res_tgt = entity_resolver.resolve_tag(tgt, resolved_tags)

                cypher = f"""
                MATCH (a {{id: $src}})
                MATCH (b {{id: $tgt}})
                MERGE (a)-[r:{r_type}]->(b)
                RETURN r
                """
                neo4j_client.run_query(cypher, {"src": res_src, "tgt": res_tgt})

                if neo4j_client.memory_graph is not None:
                    neo4j_client.memory_graph.add_edge(res_src, res_tgt, type=r_type)
                elements_count += 1

        logger.info(f"Successfully updated knowledge graph with {elements_count} elements for doc '{document_id}'")
        return elements_count


graph_builder = GraphBuilder()
