from ollama import embed
from ollama import chat
from pathlib import Path
from math import sqrt

def load_documents(directory):
    documents = []
    for file_path in Path(directory).rglob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append({
                "filename": file_path.name,
                "text": content
                })
    return documents

def generate_embeddings(documents):
    embeddings = []
    for doc in documents:
        response = embed(
            model="nomic-embed-text",
            input=doc["text"]
        )
        embeddings.append({
            "filename": doc["filename"],
            "text": doc["text"],
            "embedding": response["embeddings"][0]
        })
    return embeddings

embedded_documents = generate_embeddings(load_documents("LLM-evaluation-and-AI-testing-frameworks\\rag_eval\\documents"))

print(f"Total embedded documents: {len(embedded_documents)}\n")

for doc in embedded_documents:
    print(doc["filename"])
    print(doc["embedding"][:10])
    print("-" * 50)
    
def embed_query(query):
    response = embed(
        model="nomic-embed-text",
        input=query
    )
    return response["embeddings"][0]

query_embedding = embed_query("Which framework automates browsers?")
print(len(query_embedding))

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = sqrt(sum(b ** 2 for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def semantic_search(query, embedded_documents):
    query_embedding = embed_query(query)
    results = []
    for doc in embedded_documents:
        score = cosine_similarity(query_embedding, doc["embedding"])
        results.append({
            "filename": doc["filename"],
            "text": doc["text"],
            "score": score
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
query = "Which tool automates web browsers?"

print("Semantic search starting...")

results = semantic_search(query, embedded_documents)

print("Semantic search finished")


top_k = results[:3]

print(top_k)

def build_context(results):
    context = ""
    for res in results:
        context += f"Filename: {res['filename']}\n"
        context += f"Score: {res['score']:.4f}\n"
        context += f"Text: {res['text']}\n"
        context += "-" * 50 + "\n"
    return context
context = build_context(top_k)

def create_prompt(query, context):
    return f"""You are a helpful assistant.Answer ONLY using the provided context.If the answer is not contained in the context,say "I don't know."Context:{context}Question:{query}Answer:"""

def ask_llm(prompt):
    response = chat(
        model="gemma3:1b", 
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response["message"]["content"]

context = build_context(top_k)

prompt = create_prompt(query, context)

answer = ask_llm(prompt)

print("\nAnswer:")
print(answer)