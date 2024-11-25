import sys
import requests
from query_codebase import search_faiss_index
from sentence_transformers import SentenceTransformer

def query_ollama(prompt, context, model="llama2"):
    """Query Ollama with context and a prompt."""
    combined_prompt = f"{context}\n\n{prompt}"
    response = requests.post(
        "http://localhost:11434/api/v1/query",
        json={"prompt": combined_prompt, "model": model},
        headers={"Content-Type": "application/json"},
    )
    return response.json()["response"]

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
            print("No relevant results found in the codebase.")
            continue

        # Ensure results are in the expected format
        if not all(len(result) == 2 for result in results):
            print("Error: Results from FAISS index are not in the expected format. Please check metadata.")
            continue

        # Prepare context
        context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

        # Query Ollama
        response = query_ollama(query, context)
        print("\nOllama Response:")
        print(response)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interact_with_codebase.py <project_dir>")
        sys.exit(1)

    project_directory = sys.argv[1]
    interactive_session(project_directory)



# # ollama_feeder/interact_with_codebase.py
# import os
# import sys
# import requests
# from query_codebase import search_faiss_index
# from sentence_transformers import SentenceTransformer

# def query_ollama(prompt, context, model="llama2"):
#     """Query Ollama with context and a prompt."""
#     combined_prompt = f"{context}\n\n{prompt}"
#     response = requests.post(
#         "http://localhost:11434/api/v1/query",
#         json={"prompt": combined_prompt, "model": model},
#         headers={"Content-Type": "application/json"},
#     )
#     return response.json()["response"]

# def interactive_session(project_dir):
#     # Ensure paths are derived from the project directory
#     prompt_file = os.path.join(project_dir, "default_prompt.txt")
#     index_file = os.path.join(project_dir, "codebase_index.faiss")
#     metadata_file = os.path.join(project_dir, "metadata.txt")

#     # Check if required files exist
#     if not all(os.path.exists(path) for path in [prompt_file, index_file, metadata_file]):
#         print(f"Error: One or more required files are missing in {project_dir}.")
#         sys.exit(1)

#     # Load the default prompt
#     with open(prompt_file, "r") as f:
#         default_prompt = f.read().strip()

#     print("Interactive Codebase Session. Type 'exit' to quit.")
#     print(f"Using prompt: {default_prompt}")
    
#     model = SentenceTransformer('all-MiniLM-L6-v2')

#     while True:
#         query = input("\nYour question: ")
#         if query.lower() == "exit":
#             break

#         # Search the index
#         results = search_faiss_index(query, index_file, model, metadata_file)
#         print(f"Debug: Results from search_faiss_index: {results}")
#         context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

#         # Query Ollama
#         response = query_ollama(query, context)
#         print("\nOllama Response:")
#         print(response)

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python interact_with_codebase.py <project_dir>")
#         sys.exit(1)

#     project_directory = sys.argv[1]
#     if not os.path.isdir(project_directory):
#         print(f"Error: Provided project directory '{project_directory}' does not exist.")
#         sys.exit(1)

#     interactive_session(project_directory)


# # # ollama_feeder/interact_with_codebase.py
# # import sys
# # import requests
# # from query_codebase import search_faiss_index
# # from sentence_transformers import SentenceTransformer

# # def query_ollama(prompt, context, model="llama2"):
# #     """Query Ollama with context and a prompt."""
# #     combined_prompt = f"{context}\n\n{prompt}"
# #     response = requests.post(
# #         "http://localhost:11434/api/v1/query",
# #         json={"prompt": combined_prompt, "model": model},
# #         headers={"Content-Type": "application/json"},
# #     )
# #     return response.json()["response"]

# # def interactive_session(project_dir):
# #     # Load project files
# #     prompt_file = f"{project_dir}/default_prompt.txt"
# #     index_file = f"{project_dir}/codebase_index.faiss"
# #     metadata_file = f"{project_dir}/metadata.txt"

# #     with open(prompt_file, "r") as f:
# #         default_prompt = f.read().strip()

# #     print("Interactive Codebase Session. Type 'exit' to quit.")
# #     model = SentenceTransformer('all-MiniLM-L6-v2')

# #     while True:
# #         query = input("\nYour question: ")
# #         if query.lower() == "exit":
# #             break

# #         # Search the index
# #         results = search_faiss_index(query, index_file, model, metadata_file)
# #         context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

# #         # Query Ollama
# #         response = query_ollama(query, context)
# #         print("\nOllama Response:")
# #         print(response)

# # if __name__ == "__main__":
# #     if len(sys.argv) != 2:
# #         print("Usage: python interact_with_codebase.py <project_dir>")
# #         sys.exit(1)

# #     interactive_session(sys.argv[1])



# # # # ollama_feeder/interact_with_codebase.py
# # # import requests
# # # from query_codebase import search_faiss_index
# # # from sentence_transformers import SentenceTransformer

# # # def query_ollama(prompt, context, model="llama2"):
# # #     """Query Ollama with context and a prompt."""
# # #     combined_prompt = f"{context}\n\n{prompt}"
# # #     response = requests.post(
# # #         "http://localhost:11434/api/v1/query",
# # #         json={"prompt": combined_prompt, "model": model},
# # #         headers={"Content-Type": "application/json"},
# # #     )
# # #     return response.json()["response"]

# # # def interactive_session(default_prompt):
# # #     print("Interactive Codebase Session. Type 'exit' to quit.")
# # #     model = SentenceTransformer('all-MiniLM-L6-v2')
    
# # #     while True:
# # #         query = input("\nYour question: ")
# # #         if query.lower() == "exit":
# # #             break

# # #         # Search the index
# # #         results = search_faiss_index(query, "codebase_index.faiss", model, "metadata.txt")
# # #         context = "\n".join([f"{file_path}: {text}" for file_path, text in results])

# # #         # Query Ollama
# # #         response = query_ollama(query, context)
# # #         print("\nOllama Response:")
# # #         print(response)

# # # if __name__ == "__main__":
# # #     with open("default_prompt.txt", "r") as f:
# # #         default_prompt = f.read().strip()
# # #     interactive_session(default_prompt)

