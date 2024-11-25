import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_files(directory):
    """Load all text files from the directory."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        documents.append((file_path, content))
                        print(f"Loaded file: {file_path} ({len(content)} characters)")
                    else:
                        print(f"Skipped empty file: {file_path}")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    return documents

def chunk_text(file_path, content, chunk_size=500):
    """Chunk the content of a file into smaller parts."""
    if not content:
        print(f"Skipped chunking for empty content in: {file_path}")
        return []
    chunks = [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]
    print(f"Chunked {file_path} into {len(chunks)} chunks")
    return chunks

def main():
    if len(sys.argv) != 4:
        print("Usage: python prepare_codebase.py <codebase_dir> <index_file> <metadata_file>")
        sys.exit(1)

    codebase_dir = os.path.abspath(sys.argv[1])  # Convert to absolute path
    index_file = os.path.abspath(sys.argv[2])    # Convert to absolute path
    metadata_file = os.path.abspath(sys.argv[3]) # Convert to absolute path

    # Initialize model
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load and chunk files
    print(f"Loading files from directory: {codebase_dir}")
    documents = load_files(codebase_dir)
    if not documents:
        print("Error: No valid files found in the codebase directory.")
        sys.exit(1)

    print(f"Loaded {len(documents)} files. Chunking content...")
    chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

    if not chunks:
        print("Error: No valid content to process after chunking.")
        sys.exit(1)

    print(f"Generated {len(chunks)} chunks. Embedding texts...")
    texts = [chunk[1] for chunk in chunks if len(chunk) == 2 and chunk[1].strip()]
    if not texts:
        print("Error: No valid texts extracted from chunks.")
        sys.exit(1)

    # Embed chunks
    print("Embedding texts...")
    embeddings = model.encode(texts)

    # Create and save FAISS index
    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    faiss.write_index(index, index_file)

    # Save metadata
    print("Saving metadata...")
    with open(metadata_file, "w") as f:
        for chunk in chunks:
            if len(chunk) == 2 and chunk[1].strip():  # Ensure valid metadata
                f.write(f"{chunk[0]}||{chunk[1]}\n")
            else:
                print(f"Skipping invalid chunk: {chunk}")

    print("Codebase indexing complete.")

if __name__ == "__main__":
    main()


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
#             print("No relevant results found in the codebase.")
#             continue

#         # Filter valid results
#         valid_results = [result for result in results if len(result) == 2]
#         if not valid_results:
#             print("Error: No valid results returned from the FAISS index.")
#             continue

#         # Prepare context
#         context = "\n".join([f"{file_path}: {text}" for file_path, text in valid_results])

#         # Query Ollama
#         response = query_ollama(query, context)
#         print("\nOllama Response:")
#         print(response)

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python interact_with_codebase.py <project_dir>")
#         sys.exit(1)

#     project_directory = sys.argv[1]
#     interactive_session(project_directory)


# # import os
# # import sys
# # import faiss
# # import numpy as np
# # from sentence_transformers import SentenceTransformer


# # def load_files(directory):
# #     """Load all text files from the directory."""
# #     documents = []
# #     for root, _, files in os.walk(directory):
# #         for file in files:
# #             file_path = os.path.join(root, file)
# #             try:
# #                 with open(file_path, 'r', encoding='utf-8') as f:
# #                     content = f.read().strip()
# #                     if content:
# #                         documents.append((file_path, content))
# #                         print(f"Loaded file: {file_path} ({len(content)} characters)")
# #                     else:
# #                         print(f"Skipped empty file: {file_path}")
# #             except Exception as e:
# #                 print(f"Error reading file {file_path}: {e}")
# #     return documents


# # def chunk_text(file_path, content, chunk_size=500):
# #     """Chunk the content of a file into smaller parts."""
# #     if not content:
# #         print(f"Skipped chunking for empty content in: {file_path}")
# #         return []
# #     chunks = [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]
# #     print(f"Chunked {file_path} into {len(chunks)} chunks")
# #     return chunks


# # def main():
# #     if len(sys.argv) != 4:
# #         print("Usage: python prepare_codebase.py <codebase_dir> <index_file> <metadata_file>")
# #         sys.exit(1)

# #     codebase_dir = os.path.abspath(sys.argv[1])  # Convert to absolute path
# #     index_file = os.path.abspath(sys.argv[2])    # Convert to absolute path
# #     metadata_file = os.path.abspath(sys.argv[3]) # Convert to absolute path

# #     # Debugging paths
# #     print(f"Codebase directory: {codebase_dir}")
# #     print(f"Index file: {index_file}")
# #     print(f"Metadata file: {metadata_file}")

# #     # Initialize model
# #     print("Loading embedding model...")
# #     model = SentenceTransformer('all-MiniLM-L6-v2')

# #     # Load and chunk files
# #     print(f"Loading files from directory: {codebase_dir}")
# #     documents = load_files(codebase_dir)
# #     if not documents:
# #         print("Error: No valid files found in the codebase directory.")
# #         sys.exit(1)

# #     print(f"Loaded {len(documents)} files. Chunking content...")
# #     chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

# #     if not chunks:
# #         print("Error: No valid content to process after chunking.")
# #         sys.exit(1)

# #     print(f"Generated {len(chunks)} chunks. Preparing texts for embedding...")
# #     texts = [chunk[1] for chunk in chunks]
# #     if not texts:
# #         print("Error: No valid texts extracted from chunks.")
# #         sys.exit(1)

# #     # Embed chunks
# #     print("Embedding texts...")
# #     try:
# #         embeddings = model.encode(texts)
# #     except Exception as e:
# #         print(f"Error during embedding: {e}")
# #         sys.exit(1)

# #     # Validate embeddings
# #     if embeddings.size == 0:
# #         print("Error: No embeddings generated. Ensure the codebase contains valid text.")
# #         sys.exit(1)

# #     # Create and save FAISS index
# #     print("Creating FAISS index...")
# #     dimension = embeddings.shape[1]
# #     index = faiss.IndexFlatL2(dimension)
# #     index.add(np.array(embeddings))
# #     faiss.write_index(index, index_file)

# #     # Save metadata
# #     print("Saving metadata...")
# #     with open(metadata_file, "w") as f:
# #         for chunk in chunks:
# #             f.write(f"{chunk[0]}||{chunk[1]}\n")

# #     print("Codebase indexing complete.")


# # if __name__ == "__main__":
# #     main()


# # # import os
# # # import sys
# # # import faiss
# # # import numpy as np
# # # from sentence_transformers import SentenceTransformer

# # # def load_files(directory):
# # #     """Load all text files from the directory."""
# # #     documents = []
# # #     for root, _, files in os.walk(directory):
# # #         for file in files:
# # #             file_path = os.path.join(root, file)
# # #             try:
# # #                 with open(file_path, 'r', encoding='utf-8') as f:
# # #                     content = f.read().strip()
# # #                     if content:  # Only include non-empty files
# # #                         documents.append((file_path, content))
# # #                         print(f"Loaded file: {file_path} ({len(content)} characters)")
# # #                     else:
# # #                         print(f"Skipped empty file: {file_path}")
# # #             except Exception as e:
# # #                 print(f"Error reading file {file_path}: {e}")
# # #     return documents

# # # def chunk_text(file_path, content, chunk_size=500):
# # #     """Chunk the content of a file into smaller parts."""
# # #     if not content:
# # #         print(f"Skipped chunking for empty content in: {file_path}")
# # #         return []
# # #     chunks = [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]
# # #     print(f"Chunked {file_path} into {len(chunks)} chunks")
# # #     return chunks

# # # def main():
# # #     if len(sys.argv) != 4:
# # #         print("Usage: python prepare_codebase.py <codebase_dir> <index_file> <metadata_file>")
# # #         sys.exit(1)

# # #     codebase_dir = sys.argv[1]
# # #     index_file = sys.argv[2]
# # #     metadata_file = sys.argv[3]

# # #     # Initialize model
# # #     print("Loading embedding model...")
# # #     model = SentenceTransformer('all-MiniLM-L6-v2')

# # #     # Load and chunk files
# # #     print(f"Loading files from directory: {codebase_dir}")
# # #     documents = load_files(codebase_dir)
# # #     if not documents:
# # #         print("Error: No valid files found in the codebase directory.")
# # #         sys.exit(1)

# # #     print(f"Loaded {len(documents)} files. Chunking content...")
# # #     chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

# # #     if not chunks:
# # #         print("Error: No valid content to process after chunking.")
# # #         sys.exit(1)

# # #     print(f"Generated {len(chunks)} chunks. Preparing texts for embedding...")
# # #     texts = [chunk[1] for chunk in chunks]
# # #     if not texts:
# # #         print("Error: No valid texts extracted from chunks.")
# # #         sys.exit(1)

# # #     # Embed chunks
# # #     print("Embedding texts...")
# # #     embeddings = model.encode(texts)

# # #     # Validate embeddings
# # #     if embeddings.size == 0:
# # #         print("Error: No embeddings generated. Ensure the codebase contains valid text.")
# # #         sys.exit(1)

# # #     # Create and save FAISS index
# # #     print("Creating FAISS index...")
# # #     dimension = embeddings.shape[1]
# # #     index = faiss.IndexFlatL2(dimension)
# # #     index.add(np.array(embeddings))
# # #     faiss.write_index(index, index_file)

# # #     # Save metadata
# # #     print("Saving metadata...")
# # #     with open(metadata_file, "w") as f:
# # #         for chunk in chunks:
# # #             f.write(f"{chunk[0]}||{chunk[1]}\n")

# # #     print("Codebase indexing complete.")

# # # if __name__ == "__main__":
# # #     main()


# # # # import os
# # # # import sys
# # # # import faiss
# # # # import numpy as np
# # # # from sentence_transformers import SentenceTransformer

# # # # def load_files(directory):
# # # #     """Load all text files from the directory."""
# # # #     documents = []
# # # #     for root, _, files in os.walk(directory):
# # # #         for file in files:
# # # #             file_path = os.path.join(root, file)
# # # #             try:
# # # #                 with open(file_path, 'r', encoding='utf-8') as f:
# # # #                     content = f.read().strip()
# # # #                     if content:  # Only include non-empty files
# # # #                         documents.append((file_path, content))
# # # #                     else:
# # # #                         print(f"Skipped empty file: {file_path}")
# # # #             except Exception as e:
# # # #                 print(f"Error reading file {file_path}: {e}")
# # # #     return documents

# # # # def chunk_text(file_path, content, chunk_size=500):
# # # #     """Chunk the content of a file into smaller parts."""
# # # #     if not content:
# # # #         print(f"Skipped chunking for empty content in: {file_path}")
# # # #         return []
# # # #     return [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]

# # # # def main():
# # # #     if len(sys.argv) != 4:
# # # #         print("Usage: python prepare_codebase.py <codebase_dir> <index_file> <metadata_file>")
# # # #         sys.exit(1)

# # # #     codebase_dir = sys.argv[1]
# # # #     index_file = sys.argv[2]
# # # #     metadata_file = sys.argv[3]

# # # #     # Initialize model
# # # #     print("Loading embedding model...")
# # # #     model = SentenceTransformer('all-MiniLM-L6-v2')

# # # #     # Load and chunk files
# # # #     print(f"Loading files from directory: {codebase_dir}")
# # # #     documents = load_files(codebase_dir)
# # # #     if not documents:
# # # #         print("Error: No valid files found in the codebase directory.")
# # # #         sys.exit(1)

# # # #     print(f"Loaded {len(documents)} files. Chunking content...")
# # # #     chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

# # # #     if not chunks:
# # # #         print("Error: No valid content to process after chunking.")
# # # #         sys.exit(1)

# # # #     print(f"Generated {len(chunks)} chunks. Embedding content...")

# # # #     # Embed chunks
# # # #     texts = [chunk[1] for chunk in chunks]
# # # #     embeddings = model.encode(texts)

# # # #     # Validate embeddings
# # # #     if len(embeddings) == 0:
# # # #         print("Error: No embeddings generated. Ensure the codebase contains valid text.")
# # # #         sys.exit(1)

# # # #     # Create and save FAISS index
# # # #     print("Creating FAISS index...")
# # # #     dimension = embeddings.shape[1]
# # # #     index = faiss.IndexFlatL2(dimension)
# # # #     index.add(np.array(embeddings))
# # # #     faiss.write_index(index, index_file)

# # # #     # Save metadata
# # # #     print("Saving metadata...")
# # # #     with open(metadata_file, "w") as f:
# # # #         for chunk in chunks:
# # # #             f.write(f"{chunk[0]}||{chunk[1]}\n")

# # # #     print("Codebase indexing complete.")

# # # # if __name__ == "__main__":
# # # #     main()


# # # # # # ollama_feeder/prepare_codebase.py
# # # # # import os
# # # # # import sys
# # # # # import faiss
# # # # # import numpy as np
# # # # # from sentence_transformers import SentenceTransformer

# # # # # def load_files(directory):
# # # # #     """Load all text files from the directory."""
# # # # #     documents = []
# # # # #     for root, _, files in os.walk(directory):
# # # # #         for file in files:
# # # # #             file_path = os.path.join(root, file)
# # # # #             with open(file_path, 'r', encoding='utf-8') as f:
# # # # #                 content = f.read()
# # # # #                 documents.append((file_path, content))
# # # # #     return documents

# # # # # def chunk_text(file_path, content, chunk_size=500):
# # # # #     """Chunk the content of a file into smaller parts."""
# # # # #     return [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]

# # # # # def main():
# # # # #     if len(sys.argv) != 4:
# # # # #         print("Usage: python prepare_codebase.py <codebase_dir> <index_file> <metadata_file>")
# # # # #         sys.exit(1)

# # # # #     codebase_dir = sys.argv[1]
# # # # #     index_file = sys.argv[2]
# # # # #     metadata_file = sys.argv[3]

# # # # #     # Initialize model
# # # # #     model = SentenceTransformer('all-MiniLM-L6-v2')

# # # # #     # Load and chunk files
# # # # #     documents = load_files(codebase_dir)
# # # # #     chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

# # # # #     # Embed chunks
# # # # #     texts = [chunk[1] for chunk in chunks]
# # # # #     embeddings = model.encode(texts)

# # # # #     # Create and save FAISS index
# # # # #     dimension = embeddings.shape[1]
# # # # #     index = faiss.IndexFlatL2(dimension)
# # # # #     index.add(np.array(embeddings))
# # # # #     faiss.write_index(index, index_file)

# # # # #     # Save metadata
# # # # #     with open(metadata_file, "w") as f:
# # # # #         for chunk in chunks:
# # # # #             f.write(f"{chunk[0]}||{chunk[1]}\n")

# # # # #     print("Codebase indexing complete.")

# # # # # if __name__ == "__main__":
# # # # #     main()


# # # # # # # ollama_feeder/prepare_codebase.py
# # # # # # import os
# # # # # # import faiss
# # # # # # import numpy as np
# # # # # # from sentence_transformers import SentenceTransformer

# # # # # # def load_files(directory):
# # # # # #     """Load all text files from the directory."""
# # # # # #     documents = []
# # # # # #     for root, _, files in os.walk(directory):
# # # # # #         for file in files:
# # # # # #             file_path = os.path.join(root, file)
# # # # # #             with open(file_path, 'r', encoding='utf-8') as f:
# # # # # #                 content = f.read()
# # # # # #                 documents.append((file_path, content))
# # # # # #     return documents

# # # # # # def chunk_text(file_path, content, chunk_size=500):
# # # # # #     """Chunk the content of a file into smaller parts."""
# # # # # #     return [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]

# # # # # # def main():
# # # # # #     # Configuration
# # # # # #     codebase_dir = "./codebase"
# # # # # #     index_path = "./codebase_index.faiss"
# # # # # #     embedding_model = 'all-MiniLM-L6-v2'

# # # # # #     # Initialize model
# # # # # #     model = SentenceTransformer(embedding_model)

# # # # # #     # Load and chunk files
# # # # # #     documents = load_files(codebase_dir)
# # # # # #     chunks = [chunk for doc in documents for chunk in chunk_text(doc[0], doc[1])]

# # # # # #     # Embed chunks
# # # # # #     texts = [chunk[1] for chunk in chunks]
# # # # # #     embeddings = model.encode(texts)

# # # # # #     # Create and save FAISS index
# # # # # #     dimension = embeddings.shape[1]
# # # # # #     index = faiss.IndexFlatL2(dimension)
# # # # # #     index.add(np.array(embeddings))
# # # # # #     faiss.write_index(index, index_path)

# # # # # #     # Save metadata
# # # # # #     with open("metadata.txt", "w") as f:
# # # # # #         for chunk in chunks:
# # # # # #             f.write(f"{chunk[0]}||{chunk[1]}\n")

# # # # # #     print("Codebase indexing complete.")

# # # # # # if __name__ == "__main__":
# # # # # #     main()

