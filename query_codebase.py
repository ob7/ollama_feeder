# ollama_feeder/query_codebase.py
import faiss
import numpy as np

def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
    """Search FAISS index for the most relevant chunks."""
    print(f"Loading FAISS index from {index_file}...")
    index = faiss.read_index(index_file)

    print("Generating embedding for the query...")
    query_embedding = model.encode([query])

    print(f"Searching FAISS index for top {top_k} results...")
    distances, indices = index.search(np.array(query_embedding), top_k)

    print(f"Loading metadata from {metadata_file}...")
    metadata = []
    with open(metadata_file, "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                entry = line.strip().split("||", maxsplit=1)
                if len(entry) == 2:
                    metadata.append(entry)
                else:
                    print(f"Skipping invalid metadata entry: {entry}")

    # Match indices to metadata
    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results


# def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
#     """Search FAISS index for the most relevant chunks."""
#     # Load FAISS index
#     print(f"Loading FAISS index from {index_file}...")
#     index = faiss.read_index(index_file)

#     # Embed the query
#     print("Generating embedding for the query...")
#     # query_embedding = model.encode([query])
#     query_embedding = model.encode([query], normalize_embeddings=True)


#     # Perform search
#     print(f"Searching FAISS index for top {top_k} results...")
#     distances, indices = index.search(np.array(query_embedding), top_k)

#     # Load metadata
#     print(f"Loading metadata from {metadata_file}...")
#     with open(metadata_file, "r") as f:
#         metadata = [line.strip().split("||") for line in f.readlines()]

#     # Match indices to metadata
#     results = []
#     for idx in indices[0]:
#         if idx < len(metadata):
#             # Ensure the metadata entry has exactly two elements
#             entry = metadata[idx]
#             if len(entry) == 2:
#                 results.append((entry[0], entry[1]))
#             else:
#                 print(f"Skipping invalid metadata entry: {entry}")

#     return results
