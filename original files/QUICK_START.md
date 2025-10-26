# Quick Start Guide: Building Your First MCP Server

This guide will get you up and running with MCP servers in 15 minutes.

## What You'll Build

A working knowledge base server that Claude can use to search and retrieve documentation.

## Prerequisites

Choose your path:
- **Python**: Python 3.10+ and pip
- **TypeScript**: Node.js 18+ and npm

## Option 1: Python Implementation

### Step 1: Install Dependencies

```bash
pip install mcp pydantic
```

### Step 2: Test the Server

```bash
# Basic syntax check
python -m py_compile knowledge_base_server.py

# The server runs as a long-lived process, so test via MCP Inspector:
npx @modelcontextprotocol/inspector python knowledge_base_server.py
```

This opens a web UI where you can:
- See all available tools
- Call tools with test inputs
- View responses in real-time

### Step 3: Connect to Claude Desktop

Edit your Claude Desktop config file:

**Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "python",
      "args": ["/absolute/path/to/knowledge_base_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Important**: Use the absolute path to your server file!

### Step 4: Restart Claude Desktop

Quit and restart Claude Desktop. You should now see the knowledge base tools available.

### Step 5: Test It!

In Claude, try these prompts:

```
Can you search the knowledge base for authentication best practices?

What categories of documentation are available?

Can you get document doc-001 for me?
```

---

## Option 2: TypeScript Implementation

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Build the Server

```bash
npm run build
```

This compiles TypeScript to JavaScript in the `dist/` directory.

### Step 3: Test the Server

```bash
# Test via MCP Inspector
npx @modelcontextprotocol/inspector node dist/knowledge_base_server.js
```

### Step 4: Connect to Claude Desktop

Edit your Claude Desktop config:

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "node",
      "args": ["/absolute/path/to/dist/knowledge_base_server.js"],
      "env": {}
    }
  }
}
```

### Step 5: Restart Claude Desktop & Test

Same as Python version above!

---

## Understanding the Code

### Key Components

1. **Tool Definitions** (`list_tools`)
   - Tells Claude what tools are available
   - Includes descriptions and input schemas
   - Claude uses this to decide when to call each tool

2. **Tool Implementation** (`call_tool`)
   - Executes the actual logic
   - Validates inputs
   - Returns formatted results

3. **Input Validation**
   - Python: Pydantic models
   - TypeScript: Zod schemas
   - Automatic validation and error messages

4. **Response Formatting**
   - Support both JSON and Markdown
   - Respect character limits
   - Provide concise vs detailed options

### Example Tool Flow

```
User: "Search for authentication best practices"
    ↓
Claude: Analyzes request, decides to use search_knowledge_base
    ↓
Claude → Server: call_tool("search_knowledge_base", {query: "authentication"})
    ↓
Server: Validates input with Pydantic/Zod
    ↓
Server: Executes search logic
    ↓
Server: Formats results as Markdown
    ↓
Server → Claude: Returns formatted results
    ↓
Claude: Synthesizes response using tool data
    ↓
User: Sees natural language answer with relevant docs
```

---

## Next Steps

### 1. Modify the Example

Try these exercises:

**Easy**: Add a new field to the search results
```python
# Add an "excerpt" field showing the first sentence
```

**Medium**: Add a new tool
```python
# Create a "search_by_tag" tool that filters by tags
```

**Hard**: Connect to a real data source
```python
# Replace KNOWLEDGE_BASE with PostgreSQL queries
```

### 2. Build Your Own Server

Common use cases:

- **Database Interface**: Query your company database
- **API Wrapper**: Call internal or external APIs
- **File System**: Search and read local files
- **Integration Hub**: Combine multiple services

### 3. Production Considerations

Before deploying:

- ✅ Add proper error handling
- ✅ Implement logging
- ✅ Add authentication if needed
- ✅ Set up monitoring
- ✅ Write tests
- ✅ Document your tools well

---

## Troubleshooting

### Server Won't Start

**Problem**: Process hangs when running directly
**Solution**: MCP servers are long-lived processes. Test with MCP Inspector or Claude Desktop, not directly.

### Claude Can't See Tools

**Problem**: Tools don't appear in Claude
**Solution**: 
1. Check config file path is correct
2. Use absolute paths, not relative
3. Restart Claude Desktop
4. Check Claude Desktop logs

### Validation Errors

**Problem**: "Invalid input" errors
**Solution**: Check your input schemas match the tool descriptions. Test with MCP Inspector first.

### Import Errors (Python)

**Problem**: "ModuleNotFoundError: No module named 'mcp'"
**Solution**: 
```bash
pip install mcp pydantic
# Make sure you're using the right Python environment
```

### Build Errors (TypeScript)

**Problem**: TypeScript compilation fails
**Solution**:
```bash
# Check Node.js version
node --version  # Should be 18+

# Clean and reinstall
rm -rf node_modules dist
npm install
npm run build
```

---

## Architecture Patterns

### Pattern 1: Search + Fetch

For large datasets:
1. Search tool returns IDs + summaries
2. Fetch tool gets full details by ID

**Benefits**: Respects context limits, allows refinement

### Pattern 2: Configurable Detail Levels

```python
detail_level: Literal["concise", "detailed"]
```

Let Claude choose the right level of detail for the task.

### Pattern 3: Multiple Response Formats

```python
format: Literal["json", "markdown"]
```

- JSON: For structured data processing
- Markdown: For final user-facing responses

---

## Resources

### Documentation
- [MCP Protocol Docs](https://modelcontextprotocol.io)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

### Tools
- **MCP Inspector**: `npx @modelcontextprotocol/inspector`
- **Example Servers**: https://github.com/modelcontextprotocol/servers

### Community
- [Anthropic Developer Docs](https://docs.anthropic.com)
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/protocol/discussions)

---

## Common Questions

**Q: Can MCP servers call other MCP servers?**
A: Not directly, but you can have Claude orchestrate multiple servers.

**Q: How do I secure my MCP server?**
A: Use environment variables for secrets, validate all inputs, implement authentication.

**Q: Can I charge for my MCP server?**
A: Yes! You can build commercial MCP servers.

**Q: How do I distribute my MCP server?**
A: Publish to npm (TypeScript) or PyPI (Python), or share the code directly.

**Q: Can MCP servers modify data?**
A: Yes, but implement proper safeguards (confirmations, undo, audit logs).

**Q: What about rate limiting?**
A: Implement rate limiting in your server code. Return helpful error messages when limits are hit.

---

## What's Next?

You now understand:
✅ MCP architecture and concepts
✅ How to build a working server
✅ Tool design patterns
✅ Testing and debugging
✅ Connecting to Claude

**Your homework**: Build an MCP server for your own use case!

Ideas:
- Connect to your company's internal APIs
- Query your personal database
- Integrate with your favorite services
- Automate repetitive tasks

Remember: Start simple, iterate based on real usage, and focus on enabling workflows, not just wrapping APIs.

**Good luck, and happy building! 🚀**
