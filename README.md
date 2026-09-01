# Outreach Automation Platform

A Python-based prospect discovery and personalized outreach prototype designed to identify potential business opportunities across online communities and generate context-aware outreach using a locally hosted LLM.

## Overview

The project was built as an internal automation tool to streamline the early stages of B2B prospecting.
It combines multi-source prospect discovery, contextual data extraction, local LLM-based personalization, and structured lead storage into a single workflow.
The system currently supports prospect discovery from:

- Reddit
- Indie Hackers
- X (Twitter)

For each prospect, relevant context is collected and passed to a locally hosted Mistral 7B model to generate a personalized outreach pitch. Prospect information and generated pitches are persisted in SQLite.

> **Status:** Prototype / Work in Progress
>
> This repository represents the implemented portion of the project and is not a production-ready outreach platform.

## Workflow

```text
Online Sources
      ↓
Prospect Discovery
      ↓
Context Extraction
      ↓
Local LLM (Mistral 7B)
      ↓
Personalized Outreach Pitch
      ↓
SQLite Storage
```

## Tech Stack

- Python
- Selenium
- Requests
- BeautifulSoup
- llama.cpp 
- Mistral 7B (GGUF)
- SQLite
- JSON

## Key Components

- Prospect Discovery: Collects potential prospects and relevant contextual information from multiple online platforms.
- Context Extraction: Extracts information from posts and profiles to provide the LLM with relevant prospect context.
- AI Personalization: Uses a locally hosted Mistral 7B model through llama.cpp to generate context-aware outreach pitches with configurable styles.
- Data Persistence: Stores prospect information, source context, generated pitches, and timestamps in SQLite.

## Why I Built It

The goal was to explore how LLMs and automation could reduce the manual work involved in identifying relevant prospects and creating personalized outreach.
Rather than generating generic messages, the workflow attempts to ground each pitch in publicly available context associated with the prospect.

## Future Improvements
      
### Potential extensions include:
- Improved prospect filtering and qualification
- Additional data sources
- More robust error handling
- Outreach tracking
- Response tracking
- Campaign management
- Automated follow-up workflows
