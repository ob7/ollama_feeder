# ollama_feeder/query_codebase.py
import faiss
import numpy as np


import faiss
import numpy as np

def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
    """Search FAISS index for the most relevant chunks."""
    # Load FAISS index
    print(f"Loading FAISS index from {index_file}...")
    index = faiss.read_index(index_file)

    # Generate embedding for the query
    print("Generating embedding for the query...")
    query_embedding = model.encode([query])

    # Perform search
    print(f"Searching FAISS index for top {top_k} results...")
    distances, indices = index.search(np.array(query_embedding).astype("float32"), top_k)

    # Load metadata
    print(f"Loading metadata from {metadata_file}...")
    metadata = []
    with open(metadata_file, "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                entry = line.strip().split("||", maxsplit=1)
                if len(entry) == 2:  # Ensure proper metadata format
                    metadata.append(entry)
                else:
                    print(f"Skipping invalid metadata entry: {entry}")

    # Match indices to metadata
    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):  # Ensure index is valid
            results.append(metadata[idx])
        else:
            print(f"Skipping out-of-bounds index: {idx}")

    return results


# def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
#     """Search FAISS index for the most relevant chunks."""
#     print(f"Loading FAISS index from {index_file}...")
#     index = faiss.read_index(index_file)

#     print("Generating embedding for the query...")
#     query_embedding = model.encode([query])

#     print(f"Searching FAISS index for top {top_k} results...")
#     distances, indices = index.search(np.array(query_embedding), top_k)

#     print(f"Loading metadata from {metadata_file}...")
#     with open(metadata_file, "r") as f:
#         metadata = [line.strip().split("||") for line in f.readlines()]

#     results = []
#     for dist, idx in zip(distances[0], indices[0]):
#         if idx < len(metadata):
#             entry = metadata[idx]
#             if len(entry) == 2:  # Ensure valid entry
#                 results.append((dist, entry[0], entry[1]))

#     # Filter out low-priority or irrelevant chunks
#     filtered_results = [
#         (file_path, text) for _, file_path, text in sorted(results, key=lambda x: x[0])
#         if len(text.split()) > 10 and "TODO" not in text
#     ]

#     return filtered_results[:top_k]


# def search_faiss_index(query, index_file, model, metadata_file, top_k=5):
#     """Search FAISS index for the most relevant chunks."""
#     print(f"Loading FAISS index from {index_file}...")
#     index = faiss.read_index(index_file)

#     print("Generating embedding for the query...")
#     query_embedding = model.encode([query])

#     print(f"Searching FAISS index for top {top_k} results...")
#     distances, indices = index.search(np.array(query_embedding), top_k)

#     print(f"Loading metadata from {metadata_file}...")
#     metadata = []
#     with open(metadata_file, "r") as f:
#         for line in f:
#             if line.strip():  # Skip empty lines
#                 entry = line.strip().split("||", maxsplit=1)
#                 if len(entry) == 2:
#                     metadata.append(entry)
#                 else:
#                     print(f"Skipping invalid metadata entry: {entry}")

#     # Match indices to metadata
#     results = []
#     for idx in indices[0]:
#         if idx < len(metadata):
#             results.append(metadata[idx])

#     return results

