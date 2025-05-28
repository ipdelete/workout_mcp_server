# ADR Catalog 

Optimized ADR Index for Agent Context

## Index

| id  | title                                  | status | details                                                        |
| --- | -------------------------------------- | ------ | -------------------------------------------------------------- |
| 001 | Testing Philosophy & Strategy          | acc    | [ADR-001](001-testing-philosophy-and-strategy.md)              |
| 002 | MCP Framework Selection                | acc    | [ADR-002](002-mcp-framework-selection.md)                      |


---

## ADR Records

---------------------------------------------------------
```yaml
id: 010
title: Testing Philosophy & Strategy
status: accepted
date: 2025-05-16
decision: Behaviour‑driven tests focusing on observable outputs.
why: |
• Maintains stability through refactors
• Easier to read & write
• Reduced mocking complexity
updates: Added patterns for write‑protection & sensitive‑data tests.
tradeoffs:
positive: \[robust, readable, fast]
negative: \[initial BDD learning, more integration tests]
```
---------------------------------------------------------

--------------------------------------------
```yaml
id: 002
title: MCP Framework Selection
status: accepted
date: 2025-05-15
decision: Use FastMCP framework to implement the MCP server.
why: |
• \~70 % less boilerplate than raw MCP
• Built‑in type safety & JSON‑RPC handling
• Familiar CLI‑style pattern
• Active community & docs
tradeoffs:
positive: \[fast-dev, fewer protocol bugs, auto validation]
negative: \[framework lock‑in, less low‑level control]
```
--------------------------------------------
