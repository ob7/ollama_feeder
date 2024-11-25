# ollama_feeder/interact_with_codebase.py

import sys
import requests
from query_codebase import search_faiss_index
from sentence_transformers import SentenceTransformer


import json

def query_ollama(prompt, context, model="llama2"):
    """Query Ollama with context and a prompt."""
    combined_prompt = f"{context}\n\n{prompt}" if context else prompt
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

        return final_response.strip() if final_response else "No valid response received from the LLM."

    except requests.exceptions.RequestException as e:
        print(f"Error querying Ollama: {e}")
        return "Error querying the LLM."


# import json

# def query_ollama(prompt, context, model="llama2"):
#     """Query Ollama with context and a prompt."""
#     combined_prompt = f"{context}\n\n{prompt}" if context else prompt
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             data=json.dumps({
#                 "model": model,
#                 "prompt": combined_prompt
#             }),
#             headers={"Content-Type": "application/json"},
#         )
#         response.raise_for_status()  # Raise an error for HTTP errors

#         # Safely parse JSON response
#         try:
#             json_response = response.json()
#             return json_response.get("response", "No valid response found in JSON.")
#         except json.JSONDecodeError:
#             print(f"Error decoding JSON response: {response.text}")
#             return "Error decoding the LLM's response."

#     except requests.exceptions.RequestException as e:
#         print(f"Error querying Ollama: {e}")
#         return "Error querying the LLM."


# def query_ollama(prompt, context, model="llama2"):
#     """Query Ollama with context and a prompt."""
#     combined_prompt = f"{context}\n\n{prompt}"
#     response = requests.post(
#         "http://localhost:11434/api/v1/query",
#         json={"prompt": combined_prompt, "model": model},
#         headers={"Content-Type": "application/json"},
#     )
#     return response.json()["response"]


# def query_ollama(prompt, context="", model="llama2"):
#     """Query Ollama with or without context."""
#     combined_prompt = f"{context}\n\n{prompt}" if context else prompt
#     response = requests.post(
#         "http://localhost:11434/api/v1/query",
#         json={"prompt": combined_prompt, "model": model},
#         headers={"Content-Type": "application/json"},
#     )
#     try:
#         return response.json().get("response", "No response from the model.")
#     except Exception as e:
#         return f"Error: {e}"

# def query_ollama(prompt, context, model="llama2"):
#     """Query Ollama with context and a prompt."""
#     combined_prompt = f"{context}\n\n{prompt}" if context else prompt
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             data=json.dumps({
#                 "model": model,
#                 "prompt": combined_prompt
#             }),
#             headers={"Content-Type": "application/json"},
#         )
#         response.raise_for_status()  # Raise an error for HTTP errors
#         return response.json().get("response", "No response from Ollama.")
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying Ollama: {e}")
#         return "Error querying the LLM."


# def interactive_session(project_dir):
#     # Paths for project files
#     prompt_file = f"{project_dir}/default_prompt.txt"
#     index_file = f"{project_dir}/codebase_index.faiss"
#     metadata_file = f"{project_dir}/metadata.txt"

#     # Validate paths
#     if not all([prompt_file, index_file, metadata_file]):
#         print(f"Error: One or more required files are missing in {project_dir}.")
#         sys.exit(1)

#     # Load default prompt
#     with open(prompt_file, "r") as f:
#         default_prompt = f.read().strip()

#     print("Interactive Codebase Session. Type 'exit' to quit.")
#     print(f"Using prompt: {default_prompt}")

#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     # while True:
#     #     query = input("\nYour question: ")
#     #     if not query.strip():
#     #       print("Please enter a valid question.")
#     #       continue
#     #     if query.lower() == "exit":
#     #         break

#     #     # Search FAISS index
#     #     results = search_faiss_index(query, index_file, model, metadata_file)
#     #     if not results:
#     #         print("No relevant results found in the codebase.")
#     #         continue

#     #     # Ensure results are in the expected format
#     #     if not all(len(result) == 2 for result in results):
#     #         print("Error: Results from FAISS index are not in the expected format. Please check metadata.")
#     #         continue

#     #     # Prepare context
#     #     context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

#     #     # Query Ollama
#     #     response = query_ollama(query, context)
#     #     print("\nOllama Response:")
#     #     print(response)




#     while True:
#         query = input("\nYour question: ")
#     if query.lower() == "exit":
#         break

#     # Search FAISS index
#     results = search_faiss_index(query, index_file, model, metadata_file)
#     if not results:
#         print("No relevant results found in the codebase. Interacting with LLM only.")
#         context = ""
#     else:
#         context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

#     # Query Ollama
#     response = query_ollama(query, context)
#     print("\nOllama Response:")
#     print(response)




# def interactive_session(project_dir):
#     # Paths for project files
#     prompt_file = f"{project_dir}/default_prompt.txt"
#     index_file = f"{project_dir}/codebase_index.faiss"
#     metadata_file = f"{project_dir}/metadata.txt"

#     # Validate paths
#     if not all([prompt_file, index_file, metadata_file]):
#         print(f"Error: One or more required files are missing in {project_dir}.")
#         sys.exit(1)

#     # Load default prompt
#     with open(prompt_file, "r") as f:
#         default_prompt = f.read().strip()

#     print("Interactive Codebase Session. Type 'exit' to quit.")
#     print(f"Using prompt: {default_prompt}")

#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     while True:
#         query = input("\nYour question: ")
#         if query.lower() == "exit":
#             break

#         # Search FAISS index
#         results = search_faiss_index(query, index_file, model, metadata_file)

#         if not results:
#             print("No relevant results found in the codebase. Interacting with LLM only.")
#             context = ""  # No codebase context
#         else:
#             # Prepare context from FAISS results
#             context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

#         # Query Ollama
#         response = query_ollama(query, context or "You are an assistant. Answer questions or provide responses.")
#         print("\nOllama Response:")
#         print(response)


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
    conversation_history = default_prompt  # Initialize with the default prompt

    while True:
        query = input("\nYour question: ")
        if query.lower() == "exit":
            break

        # Search FAISS index
        results = search_faiss_index(query, index_file, model, metadata_file)
        if results:
            context = "\n".join([f"{file_path}: {text}" for file_path, text in results])
        else:
            context = None
            print("No relevant results found in the codebase. Interacting with LLM only.")

        # Add query and response to conversation history
        if context:
            conversation_history += f"\n\nContext:\n{context}"

        conversation_history += f"\n\nUser: {query}"

        # Truncate conversation history to avoid exceeding token limits
        # max_tokens = 2000  # Adjust based on your LLM's token limit
        # if len(conversation_history.split()) > max_tokens:
        #     conversation_history = " ".join(conversation_history.split()[-max_tokens:])

        # Query the LLM
        response = query_ollama(query, conversation_history)
        print("\nOllama Response:")
        print(response)

        # Append LLM's response to the history
        conversation_history += f"\nAssistant: {response}"




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interact_with_codebase.py <project_dir>")
        sys.exit(1)

    project_directory = sys.argv[1]
    interactive_session(project_directory)
