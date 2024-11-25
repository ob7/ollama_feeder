import faiss
import numpy as np

def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
    """Search FAISS index for the most relevant chunks."""
    # Load FAISS index
    print(f"Loading FAISS index from {index_file}...")
    index = faiss.read_index(index_file)

    # Embed the query
    print("Generating embedding for the query...")
    query_embedding = model.encode([query])

    # Perform search
    print(f"Searching FAISS index for top {top_k} results...")
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Load metadata
    print(f"Loading metadata from {metadata_file}...")
    with open(metadata_file, "r") as f:
        metadata = [line.strip().split("||") for line in f.readlines()]

    # Match indices to metadata
    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            # Ensure the metadata entry has exactly two elements
            entry = metadata[idx]
            if len(entry) == 2:
                results.append((entry[0], entry[1]))
            else:
                print(f"Skipping invalid metadata entry: {entry}")

    return results


# # ollama_feeder/query_codebase.py
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# # Query FAISS index
# def search_faiss_index(query, index_path, model, metadata_path, top_k=5):
#     # Load index
#     index = faiss.read_index(index_path)

#     # Load metadata
#     with open(metadata_path, "r") as f:
#         chunks = [line.strip().split("||") for line in f]

#     # Encode query
#     query_embedding = model.encode([query])

#     # Search index
#     _, indices = index.search(np.array(query_embedding), top_k)

#     # Retrieve results
#     results = [chunks[idx] for idx in indices[0]]
#     return results

# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) < 2:
#         print("Usage: python query_codebase.py '<query>'")
#         sys.exit(1)

#     query = sys.argv[1]
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     results = search_faiss_index(query, "codebase_index.faiss", model, "metadata.txt")

#     print("\nResults:")
#     for file_path, text in results:
#         print(f"File: {file_path}\nText: {text}\n")

