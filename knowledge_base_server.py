#!/usr/bin/env python3
"""
Knowledge Base MCP Server
==========================

A comprehensive example MCP server demonstrating best practices for agentic automation.

This server provides tools to search and retrieve documentation from a simulated
knowledge base, showcasing:
- Proper tool design for AI agents
- Input validation with Pydantic
- Multiple response formats (JSON and Markdown)
- Error handling and pagination
- Context-aware responses

Author: Solution Architect Tutorial
License: MIT
"""

import asyncio
import json
from datetime import datetime
from typing import Literal, Optional, List, Dict, Any
from enum import Enum

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field, ConfigDict

# ============================================================================
# CONFIGURATION
# ============================================================================

# Character limit for responses to respect Claude's context window
CHARACTER_LIMIT = 25000

# Simulated knowledge base (in production, this would be a database/API)
KNOWLEDGE_BASE = [
    {
        "id": "doc-001",
        "title": "API Authentication Best Practices",
        "category": "security",
        "content": """
        Authentication is critical for API security. Key practices include:
        
        1. Use OAuth 2.0 or JWT tokens for stateless authentication
        2. Implement rate limiting per user/token
        3. Always use HTTPS in production
        4. Rotate secrets regularly (every 90 days minimum)
        5. Implement proper token expiration (15-60 minutes for access tokens)
        6. Store refresh tokens securely
        7. Use API keys for service-to-service communication
        8. Implement request signing for sensitive operations
        
        Common pitfalls:
        - Storing tokens in localStorage (use httpOnly cookies instead)
        - Not validating token signatures
        - Overly permissive CORS policies
        - Logging sensitive authentication data
        """,
        "tags": ["authentication", "security", "api", "oauth", "jwt"],
        "created": "2024-01-15",
        "updated": "2024-10-20"
    },
    {
        "id": "doc-002",
        "title": "Microservices Communication Patterns",
        "category": "architecture",
        "content": """
        Effective microservices communication requires choosing the right pattern:
        
        Synchronous Patterns:
        - REST APIs: Simple, widely supported, but can create coupling
        - gRPC: High performance, strong typing, requires HTTP/2
        - GraphQL: Flexible querying, good for complex data requirements
        
        Asynchronous Patterns:
        - Message Queues (RabbitMQ, SQS): Reliable, decoupled, eventual consistency
        - Event Streaming (Kafka, Kinesis): High throughput, event sourcing
        - Pub/Sub (Google Pub/Sub, SNS): Fan-out patterns, loose coupling
        
        Choosing the right pattern:
        - Use async for long-running operations
        - Use sync for immediate consistency requirements
        - Consider circuit breakers for resilience
        - Implement idempotency for all operations
        - Design for failure (timeouts, retries, fallbacks)
        """,
        "tags": ["microservices", "architecture", "rest", "grpc", "messaging"],
        "created": "2024-02-10",
        "updated": "2024-09-15"
    },
    {
        "id": "doc-003",
        "title": "Database Scaling Strategies",
        "category": "database",
        "content": """
        Scaling databases requires understanding your bottlenecks:
        
        Vertical Scaling:
        - Increase CPU, RAM, or storage
        - Simple but has limits
        - Good for initial growth
        
        Horizontal Scaling:
        - Read Replicas: Offload read traffic, eventual consistency
        - Sharding: Partition data across servers, complex but unlimited scale
        - Multi-region: Geographic distribution, high availability
        
        Caching Strategies:
        - Redis/Memcached for hot data
        - CDN for static content
        - Application-level caching
        - Database query result caching
        
        When to use each:
        - Start with vertical scaling and read replicas
        - Add caching when read-heavy
        - Consider sharding only when necessary (adds complexity)
        - Use time-series databases for metrics/logs
        """,
        "tags": ["database", "scaling", "performance", "redis", "sharding"],
        "created": "2024-03-05",
        "updated": "2024-10-01"
    },
    {
        "id": "doc-004",
        "title": "Event-Driven Architecture Patterns",
        "category": "architecture",
        "content": """
        Event-driven architecture enables loose coupling and scalability:
        
        Core Concepts:
        - Events: Immutable facts about state changes
        - Event Producers: Services that emit events
        - Event Consumers: Services that react to events
        - Event Store: Persistent log of all events
        
        Key Patterns:
        1. Event Sourcing: Store events as source of truth
        2. CQRS: Separate read and write models
        3. Saga Pattern: Manage distributed transactions
        4. Event Notification: Simple pub/sub
        5. Event-Carried State Transfer: Include state in events
        
        Benefits:
        - Loose coupling between services
        - Easy to add new consumers
        - Natural audit trail
        - Supports event replay and debugging
        
        Challenges:
        - Eventual consistency
        - Event schema evolution
        - Debugging distributed flows
        - Ensuring event ordering when needed
        """,
        "tags": ["event-driven", "architecture", "cqrs", "event-sourcing", "saga"],
        "created": "2024-04-12",
        "updated": "2024-10-10"
    },
    {
        "id": "doc-005",
        "title": "Container Orchestration with Kubernetes",
        "category": "devops",
        "content": """
        Kubernetes orchestrates containerized applications at scale:
        
        Core Components:
        - Pods: Smallest deployable units
        - Deployments: Manage pod replicas
        - Services: Network access to pods
        - Ingress: External access routing
        - ConfigMaps/Secrets: Configuration management
        
        Best Practices:
        - Use namespaces for isolation
        - Set resource requests and limits
        - Implement health checks (liveness/readiness)
        - Use Horizontal Pod Autoscaling
        - Store secrets in external vaults (not etcd)
        - Implement network policies
        - Use StatefulSets for stateful apps
        - Version your manifests in Git
        
        Common Patterns:
        - Sidecar: Helper containers in pods
        - Ambassador: Proxy for external services
        - Adapter: Standardize output
        - Init Containers: Setup before main container
        """,
        "tags": ["kubernetes", "containers", "devops", "orchestration", "docker"],
        "created": "2024-05-20",
        "updated": "2024-10-05"
    }
]

# ============================================================================
# DATA MODELS
# ============================================================================

class ResponseFormat(str, Enum):
    """Response format options"""
    JSON = "json"
    MARKDOWN = "markdown"


class DetailLevel(str, Enum):
    """Detail level for responses"""
    CONCISE = "concise"
    DETAILED = "detailed"


class SearchInput(BaseModel):
    """Input model for search_knowledge_base tool"""
    model_config = ConfigDict(extra='forbid')
    
    query: str = Field(
        description="Search query to find relevant documentation. Can include keywords, phrases, or specific topics.",
        min_length=1,
        max_length=500,
        examples=["authentication best practices", "kubernetes scaling", "event-driven patterns"]
    )
    
    category: Optional[str] = Field(
        default=None,
        description="Optional category filter. Available categories: security, architecture, database, devops",
        examples=["security", "architecture", None]
    )
    
    max_results: int = Field(
        default=5,
        description="Maximum number of results to return",
        ge=1,
        le=10
    )
    
    format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Response format: 'json' for structured data, 'markdown' for human-readable text"
    )
    
    detail_level: DetailLevel = Field(
        default=DetailLevel.CONCISE,
        description="Detail level: 'concise' for summaries, 'detailed' for full content"
    )


class GetDocumentInput(BaseModel):
    """Input model for get_document tool"""
    model_config = ConfigDict(extra='forbid')
    
    document_id: str = Field(
        description="Unique identifier of the document to retrieve",
        examples=["doc-001", "doc-002"]
    )
    
    format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Response format: 'json' for structured data, 'markdown' for human-readable text"
    )


class ListCategoriesInput(BaseModel):
    """Input model for list_categories tool"""
    model_config = ConfigDict(extra='forbid')
    
    format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Response format: 'json' for structured data, 'markdown' for human-readable text"
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def truncate_text(text: str, max_chars: int = CHARACTER_LIMIT) -> str:
    """Truncate text to maximum character limit"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 50] + "\n\n[Content truncated to fit context limit]"


def format_document_markdown(doc: Dict[str, Any], detail_level: DetailLevel) -> str:
    """Format a document as Markdown"""
    lines = [
        f"## {doc['title']}",
        f"**ID:** {doc['id']}",
        f"**Category:** {doc['category']}",
        f"**Tags:** {', '.join(doc['tags'])}",
        f"**Last Updated:** {doc['updated']}",
        ""
    ]
    
    if detail_level == DetailLevel.DETAILED:
        lines.append("### Content")
        lines.append(doc['content'].strip())
    else:
        # Concise: just first paragraph
        content_lines = [line.strip() for line in doc['content'].strip().split('\n') if line.strip()]
        first_para = content_lines[0] if content_lines else ""
        lines.append(f"**Summary:** {first_para}")
    
    return "\n".join(lines)


def calculate_relevance_score(doc: Dict[str, Any], query: str) -> float:
    """Calculate a simple relevance score for a document"""
    query_lower = query.lower()
    score = 0.0
    
    # Title match (highest weight)
    if query_lower in doc['title'].lower():
        score += 10.0
    
    # Content match
    content_matches = doc['content'].lower().count(query_lower)
    score += content_matches * 2.0
    
    # Tag matches
    for tag in doc['tags']:
        if query_lower in tag.lower():
            score += 5.0
    
    # Category match
    if query_lower in doc['category'].lower():
        score += 3.0
    
    return score


async def search_documents(
    query: str,
    category: Optional[str] = None,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search knowledge base and return relevant documents.
    
    In production, this would query a real database or search engine.
    This simulation demonstrates the pattern.
    """
    # Simulate async I/O (in production, this would be a database query)
    await asyncio.sleep(0.01)
    
    # Filter by category if specified
    documents = KNOWLEDGE_BASE
    if category:
        documents = [doc for doc in documents if doc['category'].lower() == category.lower()]
    
    # Calculate relevance scores
    scored_docs = [
        (doc, calculate_relevance_score(doc, query))
        for doc in documents
    ]
    
    # Sort by relevance and limit results
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    results = [doc for doc, score in scored_docs if score > 0][:max_results]
    
    return results


async def get_document_by_id(document_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a specific document by ID"""
    await asyncio.sleep(0.01)  # Simulate async I/O
    
    for doc in KNOWLEDGE_BASE:
        if doc['id'] == document_id:
            return doc
    return None


def get_all_categories() -> List[str]:
    """Get list of all unique categories"""
    categories = set(doc['category'] for doc in KNOWLEDGE_BASE)
    return sorted(categories)


# ============================================================================
# MCP SERVER INITIALIZATION
# ============================================================================

# Initialize the MCP server
server = Server("knowledge-base-server")


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="search_knowledge_base",
            description="""
Search the knowledge base for relevant documentation and best practices.

This tool searches across titles, content, tags, and categories to find the most relevant documents.
Use this when you need to find information about specific topics, technologies, or patterns.

**When to use:**
- Finding best practices for a technology or pattern
- Looking up documentation on specific topics
- Discovering related content by keywords

**Parameters:**
- query: Keywords or phrases to search for (required)
- category: Filter by category (optional): security, architecture, database, devops
- max_results: Number of results to return (1-10, default: 5)
- format: Response format - 'json' or 'markdown' (default: markdown)
- detail_level: 'concise' for summaries or 'detailed' for full content (default: concise)

**Returns:**
- Markdown or JSON formatted list of relevant documents with relevance-ranked results
- Each result includes title, ID, category, tags, and content (based on detail_level)
- Empty result if no relevant documents found

**Example usage:**
- "Search for authentication best practices" → search_knowledge_base(query="authentication", detail_level="detailed")
- "Find microservices patterns" → search_knowledge_base(query="microservices", category="architecture")
            """.strip(),
            inputSchema=SearchInput.model_json_schema()
        ),
        Tool(
            name="get_document",
            description="""
Retrieve a specific document by its unique identifier.

Use this tool when you have a document ID (from search results) and want to retrieve the full content.
This is more efficient than searching when you know exactly which document you need.

**When to use:**
- After getting a document ID from search results
- When referencing a specific document by ID
- To get complete, untruncated document content

**Parameters:**
- document_id: The unique ID of the document (e.g., "doc-001")
- format: Response format - 'json' or 'markdown' (default: markdown)

**Returns:**
- Complete document with full content, metadata, and tags
- Error message if document ID not found

**Error handling:**
- If document not found, returns clear message suggesting to search instead
- Include the invalid ID in error message for debugging

**Example usage:**
- get_document(document_id="doc-001") → Returns full authentication best practices document
            """.strip(),
            inputSchema=GetDocumentInput.model_json_schema()
        ),
        Tool(
            name="list_categories",
            description="""
List all available documentation categories in the knowledge base.

Use this to discover what categories of documentation are available before searching.
Helpful for understanding the scope of the knowledge base.

**When to use:**
- User asks "what topics are covered?"
- Before performing filtered searches
- To help users understand available content

**Parameters:**
- format: Response format - 'json' or 'markdown' (default: markdown)

**Returns:**
- List of all unique categories
- Document count per category

**Example usage:**
- list_categories() → Returns: security, architecture, database, devops
            """.strip(),
            inputSchema=ListCategoriesInput.model_json_schema()
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from Claude"""
    
    try:
        if name == "search_knowledge_base":
            # Validate input
            search_input = SearchInput(**arguments)
            
            # Perform search
            results = await search_documents(
                query=search_input.query,
                category=search_input.category,
                max_results=search_input.max_results
            )
            
            if not results:
                response = f"No documents found matching query: '{search_input.query}'"
                if search_input.category:
                    response += f" in category '{search_input.category}'"
                response += "\n\nTry:\n- Using different keywords\n- Removing category filter\n- Using broader search terms"
                return [TextContent(type="text", text=response)]
            
            # Format response
            if search_input.format == ResponseFormat.JSON:
                # JSON response
                json_results = [
                    {
                        "id": doc['id'],
                        "title": doc['title'],
                        "category": doc['category'],
                        "tags": doc['tags'],
                        "updated": doc['updated'],
                        "content": doc['content'].strip() if search_input.detail_level == DetailLevel.DETAILED else doc['content'].split('\n')[0].strip()
                    }
                    for doc in results
                ]
                response_text = json.dumps({
                    "query": search_input.query,
                    "results_count": len(results),
                    "documents": json_results
                }, indent=2)
            else:
                # Markdown response
                lines = [
                    f"# Search Results for: {search_input.query}",
                    f"Found {len(results)} relevant document(s)",
                    ""
                ]
                
                for i, doc in enumerate(results, 1):
                    lines.append(f"### Result {i}")
                    lines.append(format_document_markdown(doc, search_input.detail_level))
                    lines.append("")
                
                response_text = "\n".join(lines)
            
            # Truncate if needed
            response_text = truncate_text(response_text)
            
            return [TextContent(type="text", text=response_text)]
        
        elif name == "get_document":
            # Validate input
            doc_input = GetDocumentInput(**arguments)
            
            # Get document
            doc = await get_document_by_id(doc_input.document_id)
            
            if not doc:
                response = f"Document not found: {doc_input.document_id}\n\n"
                response += "This document ID does not exist in the knowledge base.\n"
                response += "Try using 'search_knowledge_base' to find relevant documents."
                return [TextContent(type="text", text=response)]
            
            # Format response
            if doc_input.format == ResponseFormat.JSON:
                response_text = json.dumps(doc, indent=2)
            else:
                response_text = format_document_markdown(doc, DetailLevel.DETAILED)
            
            # Truncate if needed
            response_text = truncate_text(response_text)
            
            return [TextContent(type="text", text=response_text)]
        
        elif name == "list_categories":
            # Validate input
            cat_input = ListCategoriesInput(**arguments)
            
            # Get categories with counts
            categories = {}
            for doc in KNOWLEDGE_BASE:
                cat = doc['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            # Format response
            if cat_input.format == ResponseFormat.JSON:
                response_text = json.dumps({
                    "categories": [
                        {"name": cat, "document_count": count}
                        for cat, count in sorted(categories.items())
                    ],
                    "total_categories": len(categories),
                    "total_documents": len(KNOWLEDGE_BASE)
                }, indent=2)
            else:
                lines = [
                    "# Knowledge Base Categories",
                    f"Total documents: {len(KNOWLEDGE_BASE)}",
                    ""
                ]
                
                for cat, count in sorted(categories.items()):
                    lines.append(f"- **{cat}**: {count} document(s)")
                
                response_text = "\n".join(lines)
            
            return [TextContent(type="text", text=response_text)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        # Provide helpful error messages
        error_msg = f"Error executing tool '{name}': {str(e)}\n\n"
        error_msg += "Please check:\n"
        error_msg += "- All required parameters are provided\n"
        error_msg += "- Parameter types and values are correct\n"
        error_msg += "- Parameter values are within allowed ranges"
        
        return [TextContent(type="text", text=error_msg)]


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
