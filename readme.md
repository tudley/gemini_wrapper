# Gemini Wrapper

A lightweight Python wrapper around LLM providers, beginning with Gemini, with the long-term goal of exposing a provider-agnostic interface for AI interactions and tool calling.

> **Status:** Early proof of concept. The current focus is architecture and learning rather than features.

---

## Goals

* Learn how modern LLM APIs work internally.
* Build a clean abstraction over multiple providers.
* Keep business logic independent of any specific AI provider.
* Avoid "magic" where possible and understand the underlying mechanisms.

---

## Current Architecture

```text
Frontend
    │
    ▼
Backend
    │
    ▼
Gemini Wrapper
    │
    ▼
Gemini API
    │
    ▼
Tool Call Requested
    │
    ▼
Backend Service
    │
    ▼
Tool Result
    │
    ▼
Gemini Final Response
```

The current proof of concept uses a simple `TodoService` to demonstrate the complete tool-calling lifecycle.

---

## Key Design Decisions

### Provider-specific code stays in provider classes

Business logic should not know anything about Gemini, OpenAI or Claude.

Instead:

```text
Business Logic
      │
      ▼
Tool Metadata
      │
      ▼
Provider Adapter
```

This allows additional providers to be added without modifying application logic.

---

### Automatic Tool Generation

Rather than manually writing tool definitions, the project explores generating them automatically from Python methods.

Current techniques:

* `inspect.signature()` for parameters
* `inspect.getdoc()` for descriptions
* `docstring-parser` for parsing Google-style docstrings
* `typing.get_origin()` / `get_args()` for handling `Literal` and other generic types

---

### Business Logic First

Services expose normal Python methods.

The AI layer discovers those methods and converts them into provider-specific tool definitions.

The goal is to write business logic once and expose it to multiple LLM providers.

---

## Current Roadmap

* [ ] Automatic tool metadata generation
* [ ] Generic `ToolMetadata` representation
* [ ] Gemini adapter
* [ ] Tool execution pipeline
* [ ] Conversation management
* [ ] OpenAI support
* [ ] Claude support
* [ ] Persistent storage
* [ ] Strava AI backend integration

---

## Philosophy

This project is as much about understanding AI APIs as it is about building one.

Where practical, the implementation favours explicit code and clear architecture over framework magic so that each component can be understood, extended and replaced independently.
