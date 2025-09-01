# backend/search.py

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama  # Import the new ollama library

class RAGSystem:
    """
    A class to handle the RAG pipeline using a local LLM with Ollama for recipes.
    """
    def __init__(self, data_path="recipes.json", model_name='all-MiniLM-L6-v2'):
        """
        Initializes the RAG system.
        """
        print("Initializing RAG System with local LLM...")
        self.data_path = data_path
        self.recipes = self._load_data()
        
        # The embedding model remains the same
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Build FAISS index
        self.index = self._build_faiss_index()
        print("RAG System initialized successfully.")

    def _load_data(self):
        """Loads recipe data from the JSON file."""
        try:
            with open(self.data_path, 'r') as f:
                print(f"Loading data from {self.data_path}...")
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.data_path}")
            return []

    def _prepare_documents(self):
        """Prepares a text document for each recipe for embedding."""
        documents = []
        for recipe in self.recipes:
            doc = (
                f"Instruction: {recipe['instruction']}. "
                f"Ingredients: {recipe['input']}. "
                f"Recipe Output: {recipe['output']}. "
                f"Difficulty: {recipe['difficulty']}. "
                f"Cuisine: {recipe['cuisine']}."
            )
            documents.append(doc)
        return documents

    def _build_faiss_index(self):
        """Builds a FAISS index for efficient similarity search."""
        print("Preparing documents for indexing...")
        documents = self._prepare_documents()
        if not documents:
            print("No documents to index.")
            return None
            
        print("Generating embeddings for all documents...")
        embeddings = self.embedding_model.encode(documents, convert_to_tensor=False)
        embeddings = np.array(embeddings).astype('float32')
        
        d = embeddings.shape[1]
        print(f"Building FAISS index with dimension {d}...")
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        print(f"FAISS index built with {index.ntotal} vectors.")
        return index

    def retrieve(self, query, k=3):
        """Retrieves the top-k most relevant recipes for a given query."""
        if self.index is None:
            print("FAISS index is not available.")
            return []
            
        print(f"Retrieving top {k} results for query: '{query}'")
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        retrieved_recipes = [self.recipes[i] for i in indices[0]]
        print(f"Retrieved {len(retrieved_recipes)} recipes.")
        return retrieved_recipes

    def generate_response(self, query, retrieved_recipes):
        """
        Generates a natural language response using a local LLM via Ollama.
        """
        if not retrieved_recipes:
            return "I couldn't find any recipes for your ingredients. Try rephrasing?"

        context = "You are a helpful recipe assistant. Suggest recipes based on the user's query and the recipe dataset.\n\n"
        context += f"User Query: \"{query}\"\n\n"
        context += "Here are some relevant recipes I found:\n\n"

        for i, recipe in enumerate(retrieved_recipes, 1):
            context += f"--- Recipe {i} ---\n"
            context += f"Instruction: {recipe['instruction']}\n"
            context += f"Ingredients: {recipe['input']}\n"
            context += f"Sample Output: {recipe['output']}\n"
            context += f"Difficulty: {recipe['difficulty']}\n"
            context += f"Cuisine: {recipe['cuisine']}\n\n"

        context += "Please recommend the best recipe based on the query."

        print("Generating response with local LLM (Ollama)...")
        try:
            response = ollama.chat(
                model='llama3',
                messages=[{'role': 'user', 'content': context}],
                options={"temperature": 0.2}
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama error: {e}")
            return "Sorry, I cannot generate a recipe right now. Please check if Ollama is running."

    def process_query(self, query):
        """Processes a user query through the full RAG pipeline."""
        print(f"\nProcessing new query: '{query}'")
        retrieved_docs = self.retrieve(query, k=3)
        final_response = self.generate_response(query, retrieved_docs)
        print("Response generated.")
        return final_response
