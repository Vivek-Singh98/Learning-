# RAG (Retrieval-Augmented Generation)

## Definition

**RAG (Retrieval-Augmented Generation)** is a technique for optimizing the output of an LLM by having it **reference an authoritative external knowledge base** — data *outside* its original training data — **before generating a response**, instead of relying only on what it memorized during training.

---

## The Problem RAG Solves

### How a normal LLM call works
```
User --> (Query + Prompt) --> LLM (trained on billions of data points) --> Output
```

An LLM is trained on a **fixed, specific set of data** up to a certain point in time. If you ask it about information that was **not part of its training data** (e.g. your personal/private documents, or anything after its training cutoff), it doesn't actually "know" the answer — but it will still try to generate one.

### Disadvantages of relying on the LLM alone

1. **Hallucination** — When the LLM doesn't have the real answer in its trained knowledge, it can confidently generate an answer that *sounds* correct but is factually wrong or made up.
2. **Not trained on your personal/private data** — The LLM has no knowledge of your own documents, company data, or domain-specific information. Fine-tuning the model every time new data comes in is **expensive, slow, and impractical** to do repeatedly. RAG avoids this by letting the LLM "look up" the relevant data at query time instead of needing to be retrained on it.

RAG solves both problems by giving the LLM access to relevant, accurate, up-to-date external information **at the time of the query**, rather than baking all knowledge permanently into the model's weights.

---

## How RAG Works — Two Pipelines

### 1. Data Ingestion Pipeline
This pipeline prepares your external knowledge base *before* any user query happens:

```
Data Ingestion --> Data Parsing --> Embedding --> Vector Store
```

- **Data Ingestion**: Bringing in raw source data (documents, PDFs, web pages, databases, etc.) into the system.
- **Data Parsing**: Breaking down and cleaning that raw data into usable, structured chunks of text.
- **Embedding**: Converting each chunk of text into a numerical vector (an embedding) that captures its semantic meaning.
- **Vector Store**: Storing these embeddings in a vector database, so they can be efficiently searched later based on similarity.

### 2. Retrieval Pipeline
This pipeline runs *at query time*, when a user actually asks something:

```
User Query --> Retrieval (search Vector Store) --> Relevant Chunks --> LLM --> Output
```

- **User Query**: The question or prompt the user submits.
- **Retrieval**: The query is embedded the same way as the stored data, and the vector store is searched to find the most semantically relevant chunks of information.
- **LLM Output**: The retrieved relevant chunks are passed to the LLM *along with* the user's query, so the LLM generates its response grounded in this real, external information — rather than relying purely on its trained-in knowledge.
