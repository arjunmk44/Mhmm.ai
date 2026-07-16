from typing import Dict, List, Any
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    id: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str


class GraphNeighborhoodResponse(BaseModel):
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)

