Ollama Feeder

Ollama Feeder is a Python-based project designed to enable Retrieval-Augmented Generation (RAG) with a local LLM (Large Language Model) using Ollama. This tool allows users to interact with a codebase by asking natural language questions, retrieving relevant information from the codebase, and integrating the responses with an LLM for intelligent contextual answers.

Note that this is my first try go at implementing RAG with Ollama and currently is not the best.  It works but needs alot of improvment.

Features:
- Codebase Indexing: Automatically indexes a codebase directory using FAISS and stores metadata for efficient searching.
- Contextual Q&A: Retrieves relevant code snippets and integrates them into the LLM query for context-aware responses.
- Memory Management: Maintains conversation history for ongoing interactions.
- Streaming LLM Responses: Streams responses from the LLM for a real-time conversational experience.

Setup:
1. Clone the Repository:
   git clone <repository_url>
   cd ollama_feeder

2. Set Up the Nix Shell ( or use pip if your not on NixOS ):
   Ensure you have Nix installed on your system. Enter the development environment using:
   nix-shell

3. Prepare a Project Directory:
   Run the setup script to initialize a project directory and prepare the FAISS index for your codebase:
   ./setup_project.sh <project_name> <codebase_path_or_repo_url>
   Replace <project_name> with a name for your project.
   Replace <codebase_path_or_repo_url> with either a local directory path or a Git repository URL.

4. Start Interacting:
   Use the interactive session script to ask questions about the indexed codebase:
   python interact_with_codebase.py <project_directory>

How It Works:
1. Setup:
   The setup_project.sh script indexes a codebase by chunking files, embedding the chunks, and storing metadata and a FAISS index. A default prompt is created for interacting with the project.

2. Querying:
   The interact_with_codebase.py script lets you ask questions about the codebase. Relevant snippets are retrieved using FAISS and provided as context to the LLM for generating intelligent responses.

3. Memory:
   Conversation history is maintained to enhance interaction, providing memory for ongoing discussions with the LLM.

Dependencies:
Dependencies are defined in the shell.nix file, which includes:
- Python
- Sentence Transformers (sentence-transformers)
- FAISS
- Ollama

Activate the development environment using nix-shell, and all dependencies will be automatically available.

Example Usage:
# Initialize a project
./setup_project.sh my_project /path/to/codebase
or
./setup_project.sh and follow prompts

# Interact with the codebase
python interact_with_codebase.py projects/my_project

this is triggered automatically when first doing project setup

Sample Interaction:

Interactive Codebase Session. Type 'exit' to quit.

Using prompt: You are an assistant knowledgeable about the given codebase. Answer questions and provide insights.

Your question: What does the main.py file do?

Ollama Response:

The main.py file is responsible for initializing the application, handling CLI arguments, and invoking core functions from the utils module.
