"""
Graph Search module for relationship-based entity neighborhood retrieval.
"""

from typing import List, Dict, Any
from ai_ml.graph.neo4j_client import neo4j_client
from ai_ml.utils.helpers import extract_equipment_tags_regex


class GraphSearch:

    def search(self, query_text: str, depth: int = 1) -> List[Dict[str, Any]]:
        """
        Extracts equipment tags from query and fetches graph neighborhoods.
        """
        query_tags = extract_equipment_tags_regex(query_text)
        if not query_tags:
            return []

        results = []
        for tag in query_tags:
            neighborhood = neo4j_client.get_neighborhood(tag, depth=depth)
            nodes = neighborhood.get("nodes", [])
            edges = neighborhood.get("edges", [])

            if nodes or edges:
                node_summary = ", ".join([f"{n.get('label')}:{n.get('id')}" for n in nodes[:5]])
                edge_summary = ", ".join([f"{e.get('source')}--[{e.get('type')}]-->{e.get('target')}" for e in edges[:5]])
                
                text_desc = f"Equipment Tag '{tag}' Neighborhood: Nodes=[{node_summary}], Connections=[{edge_summary}]"
                results.append({
                    "type": "graph",
                    "doc_id": f"graph-{tag}",
                    "text": text_desc,
                    "score": 0.90,
                    "source": f"Neo4j Knowledge Graph (Tag: {tag})"
                })

        return results


graph_search = GraphSearch()
