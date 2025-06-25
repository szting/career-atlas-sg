# RAG Implementation Plan for SG Career Atlas

## Overview
This document outlines a step-by-step approach to implement RAG (Retrieval-Augmented Generation) for the SG Career Atlas application, leveraging the Singapore Skills Framework data.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                         │
│                    (Streamlit Chat/Search)                    │
└─────────────────────┬───────────────────────┬────────────────┘
                      │                       │
                      ▼                       ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│      Query Processing       │ │      Response Generation     │
│   (Intent Classification)   │ │    (LLM + Context Fusion)    │
└─────────────────────────────┘ └─────────────────────────────┘
                      │                       ▲
                      ▼                       │
┌─────────────────────────────────────────────────────────────┐
│                    Semantic Search Engine                     │
│              (Vector DB + Hybrid Search)                      │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Base                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │  Job Roles  │ │   Skills    │ │   Relationships     │   │
│  │  Embeddings │ │ Embeddings  │ │   (Job↔Skills)      │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Data Preparation & Processing

### Step 1.1: Data Integration Pipeline
```python
# data_processor.py
import pandas as pd
import json
from typing import Dict, List, Tuple

class SkillsDataProcessor:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.job_roles_df = None
        self.skills_df = None
        self.mappings_df = None
    
    def load_all_data(self):
        """Load and integrate all CSV files"""
        # Load job roles
        self.job_roles_cwf = pd.read_csv(f"{self.data_dir}/jobsandskills-Job Role_CWF_KT.csv")
        self.job_roles_tcs = pd.read_csv(f"{self.data_dir}/jobsandskills-Job Role_TCS_CCS.csv")
        
        # Load skills data
        self.skills_data = {}
        for i in range(1, 9):
            self.skills_data[f'level_{i}'] = pd.read_csv(
                f"{self.data_dir}/jobsandskills-TSC_CCS_K_A_{i}.csv"
            )
        
        # Load mappings
        self.tsc_key = pd.read_csv(f"{self.data_dir}/jobsandskills-TSC_CCS_Key.csv")
    
    def create_unified_schema(self):
        """Create unified data structure for RAG"""
        # Implementation details in next steps
        pass
```

### Step 1.2: Document Creation for RAG
```python
# document_creator.py
from typing import List, Dict
import hashlib

class DocumentCreator:
    def create_job_role_documents(self, job_roles_df) -> List[Dict]:
        """Create searchable documents from job roles"""
        documents = []
        
        for _, row in job_roles_df.iterrows():
            doc = {
                'id': hashlib.md5(f"{row['Track']}-{row['Specialisation']}".encode()).hexdigest(),
                'type': 'job_role',
                'title': row['Specialisation'],
                'track': row['Track'],
                'track_code': row['Track Code'],
                'content': f"""
                Job Role: {row['Specialisation']}
                Track: {row['Track']}
                Description: {row.get('Description', 'N/A')}
                Required Skills: {row.get('Skills', 'N/A')}
                """,
                'metadata': {
                    'track_code': row['Track Code'],
                    'level': row.get('Level', 'N/A')
                }
            }
            documents.append(doc)
        
        return documents
    
    def create_skill_documents(self, skills_data) -> List[Dict]:
        """Create searchable documents from skills"""
        documents = []
        
        for level, df in skills_data.items():
            for _, row in df.iterrows():
                doc = {
                    'id': hashlib.md5(f"{row['TSC']}-{level}".encode()).hexdigest(),
                    'type': 'skill',
                    'title': row['TSC Title'],
                    'category': row['TSC Category'],
                    'level': level,
                    'content': f"""
                    Skill: {row['TSC Title']}
                    Category: {row['TSC Category']}
                    Proficiency Level: {row['Proficiency Level']}
                    Generic Skills: {row.get('Generic Skills (S)', 'N/A')}
                    Technical Skills: {row.get('Technical Skills and Competencies (S)', 'N/A')}
                    """,
                    'metadata': {
                        'tsc_code': row['TSC'],
                        'proficiency': row['Proficiency Level']
                    }
                }
                documents.append(doc)
        
        return documents
```

## Phase 2: Embedding & Vector Storage

### Step 2.1: Embedding Generation
```python
# embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import pickle

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, documents: List[Dict]) -> Dict[str, np.ndarray]:
        """Generate embeddings for all documents"""
        embeddings = {}
        
        # Batch process for efficiency
        texts = [doc['content'] for doc in documents]
        doc_ids = [doc['id'] for doc in documents]
        
        # Generate embeddings
        vectors = self.model.encode(texts, show_progress_bar=True)
        
        # Store with document IDs
        for doc_id, vector in zip(doc_ids, vectors):
            embeddings[doc_id] = vector
        
        return embeddings
    
    def save_embeddings(self, embeddings: Dict, filepath: str):
        """Save embeddings to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(embeddings, f)
```

### Step 2.2: Vector Database Setup
```python
# vector_store.py
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Tuple

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        # Create collections
        self.job_roles_collection = self.client.create_collection("job_roles")
        self.skills_collection = self.client.create_collection("skills")
    
    def add_documents(self, documents: List[Dict], embeddings: Dict[str, np.ndarray], 
                     collection_name: str):
        """Add documents with embeddings to vector store"""
        collection = self.client.get_collection(collection_name)
        
        # Prepare data for insertion
        ids = [doc['id'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        documents_text = [doc['content'] for doc in documents]
        embeddings_list = [embeddings[doc_id].tolist() for doc_id in ids]
        
        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadatas,
            documents=documents_text
        )
    
    def search(self, query_embedding: np.ndarray, collection_name: str, 
               n_results: int = 5) -> List[Dict]:
        """Search for similar documents"""
        collection = self.client.get_collection(collection_name)
        
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        return results
```

## Phase 3: Query Processing & Retrieval

### Step 3.1: Query Understanding
```python
# query_processor.py
from enum import Enum
from typing import Dict, List, Tuple
import re

class QueryIntent(Enum):
    JOB_SEARCH = "job_search"
    SKILL_INQUIRY = "skill_inquiry"
    CAREER_PATH = "career_path"
    SKILL_GAP = "skill_gap"
    LEARNING_RECOMMENDATION = "learning_recommendation"
    GENERAL = "general"

class QueryProcessor:
    def __init__(self, embedding_generator):
        self.embedding_generator = embedding_generator
        self.intent_patterns = {
            QueryIntent.JOB_SEARCH: [
                r"job.*in", r"career.*in", r"position.*as", r"work.*as"
            ],
            QueryIntent.SKILL_INQUIRY: [
                r"skills.*for", r"what.*skills", r"competencies.*required"
            ],
            QueryIntent.CAREER_PATH: [
                r"career.*path", r"progression", r"advance.*to"
            ],
            QueryIntent.SKILL_GAP: [
                r"skill.*gap", r"missing.*skills", r"need.*to.*learn"
            ],
            QueryIntent.LEARNING_RECOMMENDATION: [
                r"course", r"training", r"certification", r"learn"
            ]
        }
    
    def classify_intent(self, query: str) -> QueryIntent:
        """Classify user query intent"""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        return QueryIntent.GENERAL
    
    def process_query(self, query: str) -> Dict:
        """Process query and prepare for retrieval"""
        intent = self.classify_intent(query)
        query_embedding = self.embedding_generator.model.encode(query)
        
        # Extract entities (simplified version)
        entities = self.extract_entities(query)
        
        return {
            'original_query': query,
            'intent': intent,
            'embedding': query_embedding,
            'entities': entities
        }
    
    def extract_entities(self, query: str) -> Dict:
        """Extract relevant entities from query"""
        # Simplified entity extraction
        entities = {
            'skills': [],
            'job_titles': [],
            'industries': []
        }
        
        # Add more sophisticated NER here
        return entities
```

### Step 3.2: Hybrid Retrieval System
```python
# retrieval_system.py
from typing import List, Dict, Tuple
import numpy as np

class HybridRetriever:
    def __init__(self, vector_store, keyword_index):
        self.vector_store = vector_store
        self.keyword_index = keyword_index
    
    def retrieve(self, processed_query: Dict, top_k: int = 10) -> List[Dict]:
        """Perform hybrid retrieval combining semantic and keyword search"""
        
        # Semantic search
        semantic_results = self._semantic_search(
            processed_query['embedding'],
            processed_query['intent'],
            top_k
        )
        
        # Keyword search
        keyword_results = self._keyword_search(
            processed_query['original_query'],
            processed_query['entities'],
            top_k
        )
        
        # Combine and re-rank results
        combined_results = self._combine_results(
            semantic_results,
            keyword_results,
            alpha=0.7  # Weight for semantic search
        )
        
        return combined_results[:top_k]
    
    def _semantic_search(self, query_embedding: np.ndarray, 
                        intent: QueryIntent, top_k: int) -> List[Dict]:
        """Perform semantic search based on intent"""
        # Choose collection based on intent
        if intent in [QueryIntent.JOB_SEARCH, QueryIntent.CAREER_PATH]:
            collection = "job_roles"
        else:
            collection = "skills"
        
        results = self.vector_store.search(
            query_embedding,
            collection,
            n_results=top_k
        )
        
        return results
    
    def _keyword_search(self, query: str, entities: Dict, 
                       top_k: int) -> List[Dict]:
        """Perform keyword-based search"""
        # Implement BM25 or similar keyword search
        # This is a placeholder
        return []
    
    def _combine_results(self, semantic_results: List[Dict], 
                        keyword_results: List[Dict], 
                        alpha: float) -> List[Dict]:
        """Combine and re-rank results from different sources"""
        # Implement result fusion algorithm
        # This is a simplified version
        combined = semantic_results + keyword_results
        
        # Remove duplicates and re-rank
        seen = set()
        unique_results = []
        for result in combined:
            if result['id'] not in seen:
                seen.add(result['id'])
                unique_results.append(result)
        
        return unique_results
```

## Phase 4: Response Generation

### Step 4.1: Context Builder
```python
# context_builder.py
from typing import List, Dict, Tuple

class ContextBuilder:
    def __init__(self, max_context_length: int = 2000):
        self.max_context_length = max_context_length
    
    def build_context(self, query: str, retrieved_docs: List[Dict], 
                     intent: QueryIntent) -> str:
        """Build context for LLM from retrieved documents"""
        
        # Create intent-specific context
        if intent == QueryIntent.JOB_SEARCH:
            context = self._build_job_search_context(retrieved_docs)
        elif intent == QueryIntent.SKILL_INQUIRY:
            context = self._build_skill_inquiry_context(retrieved_docs)
        elif intent == QueryIntent.CAREER_PATH:
            context = self._build_career_path_context(retrieved_docs)
        else:
            context = self._build_general_context(retrieved_docs)
        
        # Add query context
        full_context = f"""
        User Query: {query}
        
        Relevant Information:
        {context}
        
        Please provide a helpful and accurate response based on the above information.
        """
        
        return full_context[:self.max_context_length]
    
    def _build_job_search_context(self, docs: List[Dict]) -> str:
        """Build context for job search queries"""
        context_parts = []
        
        for doc in docs:
            job_info = f"""
            Job Role: {doc['title']}
            Track: {doc['metadata']['track']}
            Required Skills: {doc.get('skills', 'N/A')}
            """
            context_parts.append(job_info)
        
        return "\n".join(context_parts)
```

### Step 4.2: Response Generator
```python
# response_generator.py
from typing import Dict, List
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

class ResponseGenerator:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.system_prompt = """
        You are an AI career advisor for Singapore professionals. 
        Use the provided context to give accurate, helpful career guidance.
        Base your responses on the Singapore Skills Framework data.
        Be specific and actionable in your recommendations.
        """
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_response(self, context: str, query: str) -> str:
        """Generate response using LLM"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": context}
        ]
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def format_response(self, response: str, metadata: Dict) -> Dict:
        """Format response with additional metadata"""
        return {
            'response': response,
            'sources': metadata.get('sources', []),
            'confidence': metadata.get('confidence', 0.0),
            'suggestions': metadata.get('suggestions', [])
        }
```

## Phase 5: Integration with Streamlit

### Step 5.1: RAG Service Integration
```python
# rag_service.py
from typing import Dict, List, Optional
import streamlit as st

class RAGService:
    def __init__(self):
        self.data_processor = SkillsDataProcessor("./data")
        self.doc_creator = DocumentCreator()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.query_processor = QueryProcessor(self.embedding_gen)
        self.retriever = HybridRetriever(self.vector_store, None)
        self.context_builder = ContextBuilder()
        self.response_gen = ResponseGenerator(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Initialize on first run
        if 'rag_initialized' not in st.session_state:
            self.initialize()
            st.session_state.rag_initialized = True
    
    @st.cache_resource
    def initialize(self):
        """Initialize RAG system with data"""
        # Load data
        self.data_processor.load_all_data()
        
        # Create documents
        job_docs = self.doc_creator.create_job_role_documents(
            self.data_processor.job_roles_cwf
        )
        skill_docs = self.doc_creator.create_skill_documents(
            self.data_processor.skills_data
        )
        
        # Generate embeddings
        job_embeddings = self.embedding_gen.generate_embeddings(job_docs)
        skill_embeddings = self.embedding_gen.generate_embeddings(skill_docs)
        
        # Store in vector database
        self.vector_store.add_documents(job_docs, job_embeddings, "job_roles")
        self.vector_store.add_documents(skill_docs, skill_embeddings, "skills")
    
    def process_user_query(self, query: str) -> Dict:
        """Process user query through RAG pipeline"""
        # Process query
        processed_query = self.query_processor.process_query(query)
        
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(processed_query)
        
        # Build context
        context = self.context_builder.build_context(
            query,
            retrieved_docs,
            processed_query['intent']
        )
        
        # Generate response
        response = self.response_gen.generate_response(context, query)
        
        # Format and return
        return self.response_gen.format_response(
            response,
            {
                'sources': retrieved_docs[:3],
                'confidence': 0.85,
                'suggestions': self._generate_suggestions(processed_query['intent'])
            }
        )
    
    def _generate_suggestions(self, intent: QueryIntent) -> List[str]:
        """Generate follow-up suggestions based on intent"""
        suggestions_map = {
            QueryIntent.JOB_SEARCH: [
                "What skills do I need for this role?",
                "Show me the career progression path",
                "What's the salary range?"
            ],
            QueryIntent.SKILL_INQUIRY: [
                "Where can I learn these skills?",
                "Which jobs require these skills?",
                "What's the proficiency level needed?"
            ],
            QueryIntent.CAREER_PATH: [
                "What skills should I develop next?",
                "Show me similar career paths",
                "How long does progression typically take?"
            ]
        }
        
        return suggestions_map.get(intent, [])
```

### Step 5.2: Streamlit UI Updates
```python
# Updated AI Assistant section in app.py
elif selected == "AI Assistant":
    colored_header(
        label="AI Career Assistant",
        description="Get personalized career guidance powered by RAG",
        color_name="red-70"
    )
    
    # Initialize RAG service
    if 'rag_service' not in st.session_state:
        with st.spinner("Initializing AI Assistant..."):
            st.session_state.rag_service = RAGService()
    
    rag_service = st.session_state.rag_service
    
    # Chat interface
    st.markdown("### 💬 Chat with Your AI Career Coach")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI Career Assistant powered by Singapore's Skills Framework data. I can help you with:\n\n• Finding suitable job roles\n• Understanding required skills\n• Planning career progression\n• Identifying skill gaps\n• Recommending learning resources\n\nWhat would you like to explore today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message.get("sources"):
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.markdown(f"- {source['title']} ({source['type']})")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about careers in Singapore..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = rag_service.process_user_query(prompt)
            
            st.markdown(response_data['response'])
            
            # Add to history with metadata
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_data['response'],
                "sources": response_data.get('sources', [])
            })
            
            # Show follow-up suggestions
            if response_data.get('suggestions'):
                st.markdown("**💡 You might also want to ask:**")
                cols = st.columns(len(response_data['suggestions']))
                for idx, suggestion in enumerate(response_data['suggestions']):
                    with cols[idx]:
                        if st.button(suggestion, key=f"sugg_{idx}"):
                            st.session_state.prompt_input = suggestion
                            st.experimental_rerun()
```

## Phase 6: Advanced Features

### Step 6.1: Continuous Learning
```python
# feedback_system.py
class FeedbackSystem:
    def __init__(self, storage_path: str = "./feedback"):
        self.storage_path = storage_path
    
    def collect_feedback(self, query: str, response: str, 
                        rating: int, feedback_text: str = ""):
        """Collect user feedback for continuous improvement"""
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'rating': rating,
            'feedback_text': feedback_text
        }
        
        # Store feedback for analysis
        self._store_feedback(feedback_data)
    
    def analyze_feedback(self) -> Dict:
        """Analyze feedback to identify improvement areas"""
        # Implement feedback analysis
        pass
```

### Step 6.2: Performance Monitoring
```python
# monitoring.py
import time
from functools import wraps

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'query_count': 0,
            'avg_response_time': 0,
            'avg_relevance_score': 0
        }
    
    def track_query(self, func):
        """Decorator to track query performance"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Update metrics
            self.metrics['query_count'] += 1
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['query_count'] - 1) + 
                 response_time) / self.metrics['query_count']
            )
            
            return result
        
        return wrapper
```

## Implementation Timeline

### Week 1-2: Data Preparation
- Set up data processing pipeline
- Create document structures
- Generate initial embeddings

### Week 3-4: Core RAG Implementation
- Set up vector database
- Implement retrieval system
- Integrate query processing

### Week 5-6: Response Generation
- Integrate LLM
- Build context generation
- Implement response formatting

### Week 7-8: Streamlit Integration
- Update UI components
- Add chat interface
- Implement feedback system

### Week 9-10: Testing & Optimization
- Performance testing
- Query optimization
- User acceptance testing

## Key Considerations

1. **Scalability**: Design for growing data and user base
2. **Latency**: Optimize for <2 second response times
3. **Accuracy**: Implement relevance scoring and feedback loops
4. **Security**: Ensure data privacy and secure API usage
5. **Cost**: Monitor and optimize LLM API usage

## Next Steps

1. Set up development environment
2. Install required dependencies
3. Begin with data preparation phase
4. Implement core components iteratively
5. Test with sample queries
6. Gather feedback and iterate
