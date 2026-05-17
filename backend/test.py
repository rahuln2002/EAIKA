from app.rag.chunking import (
    FixedChunker,
    RecursiveChunker,
    SemanticChunker,
)

sample_text = """
Artificial Intelligence is transforming industries.

Machine learning enables prediction systems.

Large Language Models power modern AI applications.

RAG systems improve factual accuracy.
"""

# =====================================================
# FIXED CHUNKER
# =====================================================

fixed = FixedChunker()

fixed_chunks = fixed.chunk_text(sample_text)

print("FIXED CHUNKS:")
print(fixed_chunks)

print("\n")

# =====================================================
# RECURSIVE CHUNKER
# =====================================================

recursive = RecursiveChunker()

recursive_chunks = recursive.chunk_text(sample_text)

print("RECURSIVE CHUNKS:")
print(recursive_chunks)

print("\n")

# =====================================================
# SEMANTIC CHUNKER
# =====================================================

semantic = SemanticChunker()

semantic_chunks = semantic.chunk_text(sample_text)

print("SEMANTIC CHUNKS:")
print(semantic_chunks)
