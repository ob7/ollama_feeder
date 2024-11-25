# ollama_feeder/prepare_codebase.py
import os
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# def load_files(directory):
#     """Load all text files from the directory."""
#     documents = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read().strip()
#                     if content:
#                         documents.append((file_path, content))
#                         print(f"Loaded file: {file_path} ({len(content)} characters)")
#                     else:
#                         print(f"Skipped empty file: {file_path}")
#             except Exception as e:
#                 print(f"Error reading file {file_path}: {e}")
#     return documents


# def load_files(directory):
#     """Load all text files from the directory, ignoring hidden files and .git."""
#     documents = []
#     for root, _, files in os.walk(directory):
#         # Skip hidden directories like .git
#         if any(part.startswith('.') for part in root.split(os.sep)):
#             continue
#         for file in files:
#             # Skip hidden files
#             if file.startswith('.'):
#                 continue
#             file_path = os.path.join(root, file)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read().strip()
#                     if content:
#                         documents.append((file_path, content))
#                         print(f"Loaded file: {file_path} ({len(content)} characters)")
#                     else:
#                         print(f"Skipped empty file: {file_path}")
#             except Exception as e:
#                 print(f"Error reading file {file_path}: {e}")
#     return documents


def load_files(directory):
    """Load all text files from the directory, ignoring irrelevant files."""
    documents = []
    for root, _, files in os.walk(directory):
        if '.git' in root:
            continue  # Skip .git directory
        for file in files:
            if file.startswith('.') or file.endswith(('pyc', 'log')):  # Skip hidden/system files
                continue
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



# def chunk_text(file_path, content, chunk_size=500):
#     """Chunk the content of a file into smaller parts."""
#     if not content:
#         print(f"Skipped chunking for empty content in: {file_path}")
#         return []
#     chunks = [(file_path, content[i:i + chunk_size]) for i in range(0, len(content), chunk_size)]
#     print(f"Chunked {file_path} into {len(chunks)} chunks")
#     return chunks

# def chunk_text(file_path, content, chunk_size=500):
#     """Chunk the content of a file into smaller parts."""
#     if not content:
#         print(f"Skipped chunking for empty content in: {file_path}")
#         return []
#     chunks = [(file_path, content[i:i + chunk_size].strip()) for i in range(0, len(content), chunk_size)]
#     # Filter out chunks that are too short or empty
#     chunks = [chunk for chunk in chunks if len(chunk[1].split()) > 10]  # Example: keep chunks with >10 words
#     print(f"Chunked {file_path} into {len(chunks)} chunks")
#     return chunks

# def chunk_text(file_path, content, chunk_size=500):
#     """Chunk the content of a file into smaller parts."""
#     if not content.strip():
#         print(f"Skipped chunking for empty content in: {file_path}")
#         return []
#     # Chunk content into smaller parts without filtering out small ones
#     chunks = [(file_path, content[i:i + chunk_size].strip()) for i in range(0, len(content), chunk_size)]
#     print(f"Chunked {file_path} into {len(chunks)} chunks")
#     return chunks


def chunk_text(file_path, content, chunk_size=500):
    """Chunk the content of a file into smaller parts."""
    if not content.strip():  # Skip empty content
        print(f"Skipped chunking for empty content in: {file_path}")
        return []
    # Ensure smaller chunks are not skipped by allowing any content to pass through
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
    # embeddings = model.encode(texts)
    embeddings = model.encode(texts, normalize_embeddings=True)


    # Create and save FAISS index
    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    faiss.write_index(index, index_file)

    # Save metadata
    print("Saving metadata...")
    # with open(metadata_file, "w") as f:
    #     for chunk in chunks:
    #         if len(chunk) == 2 and chunk[1].strip():  # Ensure valid metadata
    #             f.write(f"{chunk[0]}||{chunk[1]}\n")
    #         else:
    #             print(f"Skipping invalid chunk: {chunk}")
    # with open(metadata_file, "w") as f:
    #     for chunk in chunks:
    #         if len(chunk) == 2 and chunk[1].strip() and len(chunk[1].split()) > 10:
    #             f.write(f"{chunk[0]}||{chunk[1]}\n")
    #     else:
    #         print(f"Skipping invalid or small chunk: {chunk}")

    # with open(metadata_file, "w") as f:
    #     for chunk in chunks:
    #         if len(chunk) == 2 and chunk[1].strip():  # Keep all valid non-empty chunks
    #             f.write(f"{chunk[0]}||{chunk[1]}\n")
    #     else:
    #         print(f"Skipping invalid or empty chunk: {chunk}")

    # Ensure valid metadata entries
    with open(metadata_file, "w") as f:
        for chunk in chunks:
            if len(chunk) == 2 and chunk[1].strip():  # Allow any non-empty content
                f.write(f"{chunk[0]}||{chunk[1]}\n")
        else:
            print(f"Skipping invalid chunk: {chunk}")



    print("Codebase indexing complete.")

if __name__ == "__main__":
    main()
