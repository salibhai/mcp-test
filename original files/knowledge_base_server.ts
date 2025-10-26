#!/usr/bin/env node

/**
 * Knowledge Base MCP Server - TypeScript/Node.js Implementation
 * ==============================================================
 * 
 * This is the TypeScript equivalent of the Python implementation,
 * demonstrating MCP server patterns in the Node.js ecosystem.
 * 
 * Features:
 * - Strong typing with TypeScript
 * - Input validation with Zod
 * - Async/await patterns
 * - Multiple response formats
 * - Production-ready error handling
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// ============================================================================
// CONFIGURATION
// ============================================================================

const CHARACTER_LIMIT = 25000;

// ============================================================================
// TYPES AND INTERFACES
// ============================================================================

interface Document {
  id: string;
  title: string;
  category: string;
  content: string;
  tags: string[];
  created: string;
  updated: string;
}

// Simulated knowledge base
const KNOWLEDGE_BASE: Document[] = [
  {
    id: "doc-001",
    title: "API Authentication Best Practices",
    category: "security",
    content: `
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
    `.trim(),
    tags: ["authentication", "security", "api", "oauth", "jwt"],
    created: "2024-01-15",
    updated: "2024-10-20",
  },
  {
    id: "doc-002",
    title: "Microservices Communication Patterns",
    category: "architecture",
    content: `
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
    `.trim(),
    tags: ["microservices", "architecture", "rest", "grpc", "messaging"],
    created: "2024-02-10",
    updated: "2024-09-15",
  },
  {
    id: "doc-003",
    title: "Database Scaling Strategies",
    category: "database",
    content: `
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
    `.trim(),
    tags: ["database", "scaling", "performance", "redis", "sharding"],
    created: "2024-03-05",
    updated: "2024-10-01",
  },
];

// ============================================================================
// ZOD SCHEMAS (Input Validation)
// ============================================================================

const ResponseFormatSchema = z.enum(["json", "markdown"]);
const DetailLevelSchema = z.enum(["concise", "detailed"]);

const SearchInputSchema = z
  .object({
    query: z
      .string()
      .min(1)
      .max(500)
      .describe("Search query to find relevant documentation"),
    category: z
      .string()
      .optional()
      .describe("Optional category filter: security, architecture, database, devops"),
    max_results: z
      .number()
      .min(1)
      .max(10)
      .default(5)
      .describe("Maximum number of results to return"),
    format: ResponseFormatSchema.default("markdown").describe(
      "Response format: 'json' or 'markdown'"
    ),
    detail_level: DetailLevelSchema.default("concise").describe(
      "Detail level: 'concise' for summaries or 'detailed' for full content"
    ),
  })
  .strict();

const GetDocumentInputSchema = z
  .object({
    document_id: z.string().describe("Unique identifier of the document"),
    format: ResponseFormatSchema.default("markdown").describe(
      "Response format: 'json' or 'markdown'"
    ),
  })
  .strict();

const ListCategoriesInputSchema = z
  .object({
    format: ResponseFormatSchema.default("markdown").describe(
      "Response format: 'json' or 'markdown'"
    ),
  })
  .strict();

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function truncateText(text: string, maxChars: number = CHARACTER_LIMIT): string {
  if (text.length <= maxChars) {
    return text;
  }
  return text.substring(0, maxChars - 50) + "\n\n[Content truncated to fit context limit]";
}

function formatDocumentMarkdown(
  doc: Document,
  detailLevel: "concise" | "detailed"
): string {
  const lines = [
    `## ${doc.title}`,
    `**ID:** ${doc.id}`,
    `**Category:** ${doc.category}`,
    `**Tags:** ${doc.tags.join(", ")}`,
    `**Last Updated:** ${doc.updated}`,
    "",
  ];

  if (detailLevel === "detailed") {
    lines.push("### Content");
    lines.push(doc.content);
  } else {
    const contentLines = doc.content.split("\n").filter((line) => line.trim());
    const firstPara = contentLines[0] || "";
    lines.push(`**Summary:** ${firstPara}`);
  }

  return lines.join("\n");
}

function calculateRelevanceScore(doc: Document, query: string): number {
  const queryLower = query.toLowerCase();
  let score = 0;

  // Title match (highest weight)
  if (doc.title.toLowerCase().includes(queryLower)) {
    score += 10;
  }

  // Content match
  const contentMatches = (doc.content.toLowerCase().match(new RegExp(queryLower, "g")) || [])
    .length;
  score += contentMatches * 2;

  // Tag matches
  for (const tag of doc.tags) {
    if (tag.toLowerCase().includes(queryLower)) {
      score += 5;
    }
  }

  // Category match
  if (doc.category.toLowerCase().includes(queryLower)) {
    score += 3;
  }

  return score;
}

async function searchDocuments(
  query: string,
  category?: string,
  maxResults: number = 5
): Promise<Document[]> {
  // Simulate async I/O
  await new Promise((resolve) => setTimeout(resolve, 10));

  // Filter by category if specified
  let documents = KNOWLEDGE_BASE;
  if (category) {
    documents = documents.filter(
      (doc) => doc.category.toLowerCase() === category.toLowerCase()
    );
  }

  // Calculate relevance scores
  const scoredDocs = documents
    .map((doc) => ({
      doc,
      score: calculateRelevanceScore(doc, query),
    }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, maxResults)
    .map((item) => item.doc);

  return scoredDocs;
}

async function getDocumentById(documentId: string): Promise<Document | null> {
  await new Promise((resolve) => setTimeout(resolve, 10));
  return KNOWLEDGE_BASE.find((doc) => doc.id === documentId) || null;
}

function getAllCategories(): string[] {
  const categories = new Set(KNOWLEDGE_BASE.map((doc) => doc.category));
  return Array.from(categories).sort();
}

// ============================================================================
// MCP SERVER IMPLEMENTATION
// ============================================================================

class KnowledgeBaseServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "knowledge-base-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: this.getToolDefinitions(),
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "search_knowledge_base":
            return await this.handleSearch(args);
          case "get_document":
            return await this.handleGetDocument(args);
          case "list_categories":
            return await this.handleListCategories(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        if (error instanceof z.ZodError) {
          return {
            content: [
              {
                type: "text",
                text: `Invalid input: ${error.message}\n\nPlease check parameter types and values.`,
              },
            ],
          };
        }

        return {
          content: [
            {
              type: "text",
              text: `Error executing tool '${name}': ${
                error instanceof Error ? error.message : String(error)
              }`,
            },
          ],
        };
      }
    });
  }

  private getToolDefinitions(): Tool[] {
    return [
      {
        name: "search_knowledge_base",
        description: `
Search the knowledge base for relevant documentation and best practices.

This tool searches across titles, content, tags, and categories to find the most relevant documents.
Use this when you need to find information about specific topics, technologies, or patterns.

**When to use:**
- Finding best practices for a technology or pattern
- Looking up documentation on specific topics
- Discovering related content by keywords

**Returns:**
- Markdown or JSON formatted list of relevant documents with relevance-ranked results
- Each result includes title, ID, category, tags, and content (based on detail_level)
- Empty result if no relevant documents found
        `.trim(),
        inputSchema: zodToJsonSchema(SearchInputSchema),
      },
      {
        name: "get_document",
        description: `
Retrieve a specific document by its unique identifier.

Use this tool when you have a document ID (from search results) and want to retrieve the full content.
This is more efficient than searching when you know exactly which document you need.

**Returns:**
- Complete document with full content, metadata, and tags
- Error message if document ID not found
        `.trim(),
        inputSchema: zodToJsonSchema(GetDocumentInputSchema),
      },
      {
        name: "list_categories",
        description: `
List all available documentation categories in the knowledge base.

Use this to discover what categories of documentation are available before searching.
Helpful for understanding the scope of the knowledge base.
        `.trim(),
        inputSchema: zodToJsonSchema(ListCategoriesInputSchema),
      },
    ];
  }

  private async handleSearch(args: unknown) {
    const input = SearchInputSchema.parse(args);

    const results = await searchDocuments(
      input.query,
      input.category,
      input.max_results
    );

    if (results.length === 0) {
      let response = `No documents found matching query: '${input.query}'`;
      if (input.category) {
        response += ` in category '${input.category}'`;
      }
      response +=
        "\n\nTry:\n- Using different keywords\n- Removing category filter\n- Using broader search terms";
      
      return {
        content: [{ type: "text", text: response }],
      };
    }

    let responseText: string;

    if (input.format === "json") {
      const jsonResults = results.map((doc) => ({
        id: doc.id,
        title: doc.title,
        category: doc.category,
        tags: doc.tags,
        updated: doc.updated,
        content:
          input.detail_level === "detailed"
            ? doc.content
            : doc.content.split("\n")[0].trim(),
      }));

      responseText = JSON.stringify(
        {
          query: input.query,
          results_count: results.length,
          documents: jsonResults,
        },
        null,
        2
      );
    } else {
      const lines = [
        `# Search Results for: ${input.query}`,
        `Found ${results.length} relevant document(s)`,
        "",
      ];

      results.forEach((doc, index) => {
        lines.push(`### Result ${index + 1}`);
        lines.push(formatDocumentMarkdown(doc, input.detail_level));
        lines.push("");
      });

      responseText = lines.join("\n");
    }

    responseText = truncateText(responseText);

    return {
      content: [{ type: "text", text: responseText }],
    };
  }

  private async handleGetDocument(args: unknown) {
    const input = GetDocumentInputSchema.parse(args);

    const doc = await getDocumentById(input.document_id);

    if (!doc) {
      const response =
        `Document not found: ${input.document_id}\n\n` +
        "This document ID does not exist in the knowledge base.\n" +
        "Try using 'search_knowledge_base' to find relevant documents.";

      return {
        content: [{ type: "text", text: response }],
      };
    }

    let responseText: string;

    if (input.format === "json") {
      responseText = JSON.stringify(doc, null, 2);
    } else {
      responseText = formatDocumentMarkdown(doc, "detailed");
    }

    responseText = truncateText(responseText);

    return {
      content: [{ type: "text", text: responseText }],
    };
  }

  private async handleListCategories(args: unknown) {
    const input = ListCategoriesInputSchema.parse(args);

    const categories: Record<string, number> = {};
    KNOWLEDGE_BASE.forEach((doc) => {
      categories[doc.category] = (categories[doc.category] || 0) + 1;
    });

    let responseText: string;

    if (input.format === "json") {
      responseText = JSON.stringify(
        {
          categories: Object.entries(categories)
            .sort()
            .map(([name, count]) => ({ name, document_count: count })),
          total_categories: Object.keys(categories).length,
          total_documents: KNOWLEDGE_BASE.length,
        },
        null,
        2
      );
    } else {
      const lines = [
        "# Knowledge Base Categories",
        `Total documents: ${KNOWLEDGE_BASE.length}`,
        "",
      ];

      Object.entries(categories)
        .sort()
        .forEach(([cat, count]) => {
          lines.push(`- **${cat}**: ${count} document(s)`);
        });

      responseText = lines.join("\n");
    }

    return {
      content: [{ type: "text", text: responseText }],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Knowledge Base MCP Server running on stdio");
  }
}

// Helper function to convert Zod schema to JSON Schema
function zodToJsonSchema(schema: z.ZodType): Record<string, unknown> {
  // Simplified conversion - in production use a library like zod-to-json-schema
  return schema._def as unknown as Record<string, unknown>;
}

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================

const server = new KnowledgeBaseServer();
server.run().catch(console.error);
