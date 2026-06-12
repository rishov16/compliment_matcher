import json
from sentence_transformers import SentenceTransformer

def load_local_library(filename="my_liked_songs.json"):
    """Loads the cached Spotify dataset from your harvest step."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Did you run harvest.py first?")
        return None

def run_semantic_search():
    # 1. Load your local tracks
    tracks = load_local_library()
    if not tracks:
        return

    # 2. Spin up a lightweight local embedding model
    print("Initializing semantic brain (loading local model)...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # 3. Formulate how each track looks to the AI
    # We combine title and artist so the model understands context
    corpus_texts = [f"{t['title']} by {', '.join(t['artists'])}" for t in tracks]

    print("Analyzing and indexing your music library vibe...")
    # This turns your entire library into mathematical points (embeddings)
    corpus_embeddings = model.encode(corpus_texts, convert_to_tensor=True)

    print("\n--- System Ready ---")
    
    while True:
        # 4. Grab your compliment input
        prompt = input("\nDescribe how you feel or what you want to compliment (or type 'exit'): ")
        if prompt.lower() == 'exit':
            break
            
        if not prompt.strip():
            continue

        # 5. Compute embedding for your live text prompt
        query_embedding = model.encode(prompt, convert_to_tensor=True)

        # 6. Calculate how close your prompt is to every song
        # similarity() computes the mathematical cosine similarity matrix
        similarities = model.similarity(query_embedding, corpus_embeddings)[0]

        # 7. Extract the top 3 matches
        top_results = sorted(
            range(len(similarities)), 
            key=lambda i: similarities[i], 
            reverse=True
        )[:3]

        print(f"\n✨ Top tracks that capture: \"{prompt}\"\n")
        for rank, idx in enumerate(top_results, 1):
            score = float(similarities[idx])
            track_info = tracks[idx]
            artists_str = ", ".join(track_info['artists'])
            
            # Print matching metrics along with song details
            print(f"{rank}. {track_info['title']} — {artists_str}")
            print(f"   [Vibe Match Score: {score:.2%}]")
            print(f"   Album: {track_info['album']}\n")

if __name__ == "__main__":
    run_semantic_search()