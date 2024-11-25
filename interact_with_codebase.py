# ollama_feeder/interact_with_codebase.py
import sys
import requests
from query_codebase import search_faiss_index
from sentence_transformers import SentenceTransformer
import json

# Maintain conversation history for memory
conversation_history = ""

def query_ollama(prompt, context, model="llama2"):
    """Query Ollama with context and a prompt."""
    global conversation_history

    # Combine conversation history, context, and prompt
    combined_prompt = f"""
Conversation history:
{conversation_history}

Context:
{context}

Prompt:
{prompt}
""" if context else prompt

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            data=json.dumps({
                "model": model,
                "prompt": combined_prompt
            }),
            headers={"Content-Type": "application/json"},
            stream=True,  # Enable streaming
        )
        response.raise_for_status()

        # Handle streamed response
        final_response = ""
        for line in response.iter_lines():
            if line:  # Skip empty lines
                try:
                    data = json.loads(line.decode("utf-8"))
                    final_response += data.get("response", "")
                except json.JSONDecodeError:
                    print(f"Error decoding streamed line: {line}")
                    continue

        # Update conversation history
        if final_response:
            conversation_history += f"\nUser: {prompt}\nAssistant: {final_response}\n"

            # Trim conversation history if too long
            max_tokens = 2000  # Adjust this as needed
            if len(conversation_history.split()) > max_tokens:
                conversation_history = " ".join(conversation_history.split()[-max_tokens:])

        return final_response.strip() if final_response else "No valid response received from the LLM."

    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "Error querying the LLM."

def interactive_session(project_dir):
    # Paths for project files
    prompt_file = f"{project_dir}/default_prompt.txt"
    index_file = f"{project_dir}/codebase_index.faiss"
    metadata_file = f"{project_dir}/metadata.txt"

    # Validate paths
    if not all([prompt_file, index_file, metadata_file]):
        print(f"Error: One or more required files are missing in {project_dir}.")
        sys.exit(1)

    # Load default prompt
    with open(prompt_file, "r") as f:
        default_prompt = f.read().strip()

    print("Interactive Codebase Session. Type 'exit' to quit.")
    print(f"Using prompt: {default_prompt}")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    while True:
        query = input("\nYour question: ")
        if query.lower() == "exit":
            break

        # Search FAISS index
        results = search_faiss_index(query, index_file, model, metadata_file)
        if not results:
            print("No relevant results found in the codebase. Interacting with LLM only.")
            response = query_ollama(query, default_prompt)
        else:
            # Prepare context from results
            context = "\n".join([f"{file_path}: {text[:200]}..." for file_path, text in results])
            response = query_ollama(query, context)

        print("\nOllama Response:")
        print(response)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interact_with_codebase.py <project_dir>")
        sys.exit(1)

    project_directory = sys.argv[1]
    interactive_session(project_directory)

