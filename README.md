# Ollama Feeder

A Python project for enabling Retrieval-Augmented Generation (RAG) with local LLMs using Ollama. Ask natural language questions about your codebase and get contextual answers.

**Note:** This is an initial RAG implementation with Ollama that needs improvement but is functional.

## Features

- Codebase Indexing: Automatically indexes codebase using FAISS with metadata storage
- Contextual Q&A: Retrieves relevant code snippets for context-aware LLM responses 
- Memory Management: Maintains conversation history
- Streaming LLM Responses: Real-time conversational experience

## Setup

1. Clone the repository:
```
git clone <repository_url>
cd ollama_feeder
```

2. Set up environment (Nix or pip):
```
nix-shell  # If using NixOS
```

3. Initialize project:
```
./setup_project.sh <project_name> <codebase_path_or_repo_url>
```

4. Start interacting:
```
python interact_with_codebase.py <project_directory>
```

## How It Works

1. Setup: Indexes codebase by chunking files, embedding chunks, and storing metadata/FAISS index
2. Querying: Retrieves relevant snippets using FAISS as context for LLM responses
3. Memory: Maintains conversation history for ongoing discussions

## Dependencies

Defined in shell.nix:
- Python
- Sentence Transformers
- FAISS  
- Ollama

## Example Usage

Initialize project:
```
./setup_project.sh my_project /path/to/codebase
```

Interact with codebase:
```
python interact_with_codebase.py projects/my_project
```

Sample interaction:
```
Interactive Codebase Session. Type 'exit' to quit.

Using prompt: You are an assistant knowledgeable about the given codebase. Answer questions and provide insights.

Your question: What does the main.py file do?

Ollama Response:
The main.py file is responsible for initializing the application, handling CLI arguments, and invoking core functions from the utils module.
```
