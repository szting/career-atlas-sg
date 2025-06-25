"""
Unit tests for RAG components
"""

import pytest
import numpy as np
from src.rag import (
    QueryProcessor, 
    QueryIntent,
    DocumentCreator,
    EmbeddingGenerator
)

class TestQueryProcessor:
    def setup_method(self):
        self.embedding_gen = EmbeddingGenerator()
        self.processor = QueryProcessor(self.embedding_gen)
    
    def test_intent_classification(self):
        test_cases = [
            ("I want to find a job as a data scientist", QueryIntent.JOB_SEARCH),
            ("What skills do I need for cloud computing?", QueryIntent.SKILL_INQUIRY),
            ("Show me career progression for software engineers", QueryIntent.CAREER_PATH),
            ("What skills am I missing for a senior role?", QueryIntent.SKILL_GAP),
            ("Recommend courses for Python", QueryIntent.LEARNING_RECOMMENDATION)
        ]
        
        for query, expected_intent in test_cases:
            result = self.processor.classify_intent(query)
            assert result == expected_intent
    
    def test_query_processing(self):
        query = "What skills do I need for a data scientist role?"
        result = self.processor.process_query(query)
        
        assert 'original_query' in result
        assert 'intent' in result
        assert 'embedding' in result
        assert isinstance(result['embedding'], np.ndarray)

class TestDocumentCreator:
    def setup_method(self):
        self.creator = DocumentCreator()
    
    def test_job_role_document_creation(self):
        # Mock job role data
        import pandas as pd
        mock_data = pd.DataFrame({
            'Track': ['Technology'],
            'Track Code': ['TECH001'],
            'Specialisation': ['Data Scientist'],
            'Description': ['Analyzes data'],
            'Skills': ['Python, ML']
        })
        
        docs = self.creator.create_job_role_documents(mock_data)
        
        assert len(docs) == 1
        assert docs[0]['type'] == 'job_role'
        assert docs[0]['title'] == 'Data Scientist'
        assert 'content' in docs[0]
        assert 'metadata' in docs[0]

class TestEmbeddingGenerator:
    def setup_method(self):
        self.generator = EmbeddingGenerator()
    
    def test_embedding_generation(self):
        documents = [
            {'id': '1', 'content': 'Data scientist role requires Python'},
            {'id': '2', 'content': 'Cloud architect needs AWS skills'}
        ]
        
        embeddings = self.generator.generate_embeddings(documents)
        
        assert len(embeddings) == 2
        assert '1' in embeddings
        assert '2' in embeddings
        assert isinstance(embeddings['1'], np.ndarray)
        assert embeddings['1'].shape[0] == 384  # Dimension for all-MiniLM-L6-v2

if __name__ == "__main__":
    pytest.main([__file__])
