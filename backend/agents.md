# AGENTS.md

## Project

This project is a Python wrapper around LLM providers (currently Gemini, later OpenAI and Claude).

The long-term goal is to provide a provider-agnostic interface for:
- sending prompts
- registering tools
- handling tool/function calls
- returning tool results
- streaming responses

The current focus is **not** on supporting every provider, but on designing a clean architecture that can support multiple providers later.

---

# Current POC

The current proof of concept is:

Frontend
↓
Backend
↓
Gemini API
↓
Gemini requests a tool
↓
Backend executes tool
↓
Backend returns tool result to Gemini
↓
Gemini generates final natural-language response

The backend currently contains a simple TodoService to prove tool calling works.

Persistence is intentionally ignored for now.

---

# Design philosophy

The project should avoid provider-specific logic leaking into business logic.

Business logic should not know anything about:

- Gemini
- OpenAI
- Claude
- provider-specific JSON schemas

Instead:

Business Logic
↓
Tool Metadata
↓
Provider Adapter
↓
Provider-specific tool definitions

---

# Current architecture

Currently there is:

Gemini
- wraps google-genai
- handles interactions
- converts generic metadata into Gemini ToolDicts

TodoService
- owns todo business logic
- exposes methods that may become AI tools

---

# Tool generation

Current exploration is automatic tool generation using Python introspection.

The goal is to avoid manually writing Gemini tool JSON.

Instead:

Python method
↓
inspect.signature()
↓
inspect.getdoc()
↓
docstring_parser
↓
generic metadata
↓
Gemini ToolDict

---

# Introspection

Current tools being used:

inspect.signature()

Provides:

- parameter names
- annotations
- default values

inspect.getdoc()

Provides:

- method description

docstring_parser

Parses Google-style docstrings into:

- short description
- parameter descriptions
- return descriptions

---

# Current docstring style

Google style.

Example:

```python
def add_item(
    self,
    title: str,
    priority: Literal["high", "medium", "low"] = "medium",
):
    """
    Adds a todo item.

    Args:
        title:
            Name of the task.

        priority:
            Importance of the task.
    """
```

---

# Type handling

Current helper:

annotation_to_schema(annotation)

Maps:

str
↓

{
    "type": "string"
}

int
↓

{
    "type": "integer"
}

bool
↓

{
    "type": "boolean"
}

Literal[...]

↓

{
    "type": "string",
    "enum": [...]
}

Uses:

typing.get_origin()
typing.get_args()

NOT string matching.

---

# TypedDict

We discussed using TypedDict.

Important:

TypedDict is still a dict at runtime.

Example:

```python
item["title"]
```

NOT

```python
item.title
```

TypedDict exists for static typing only.

---

# Metadata vs Gemini

Important design decision.

Metadata should ideally be provider-agnostic.

Example metadata:

ToolMetadata

contains:

- name
- description
- parameters
- Python callable

Gemini should then convert this metadata into Gemini ToolDict format.

Avoid making TodoService return Gemini-specific JSON.

---

# Current implementation status

Current code is still experimenting.

Some metadata generation currently lives near TodoService.

This is acceptable while exploring.

Refactoring into cleaner metadata classes can happen later.

Avoid premature abstraction.

---

# Future roadmap

Near-term

- automatic metadata extraction
- generic ToolMetadata representation
- Gemini adapter
- execute tool calls
- support multiple tools

Medium-term

- OpenAI adapter
- Claude adapter
- provider-independent tool execution
- conversation manager
- backend API

Long-term

Strava AI assistant

Features include:

- analysing rides
- analysing training load
- modifying backend state
- todo lists
- coaching
- artifact generation

---

# Coding preferences

Prefer:

- clean OOP
- readable code
- gradual abstraction
- understanding internals over hiding complexity

Avoid:

- unnecessary decorators too early
- unnecessary metaclasses
- excessive framework magic

The goal is educational as well as functional.

Always explain WHY a design is preferred, not just WHAT to write.