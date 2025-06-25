"""
Example usage of the RAG system for SG Career Atlas
"""

import streamlit as st
from src.rag import RAGService

def main():
    # Initialize RAG service
    rag_service = RAGService()
    
    # Example queries
    example_queries = [
        "What skills do I need to become a data scientist in Singapore?",
        "Show me career progression from junior developer to tech lead",
        "What are the technical competencies for cloud computing roles?",
        "I have Python and SQL skills, what jobs can I apply for?",
        "What's the difference between Level 3 and Level 4 proficiency?",
        "Recommend training for transitioning to cybersecurity"
    ]
    
    st.title("RAG System Demo")
    
    # Query input
    query = st.selectbox("Select an example query or type your own:", 
                        ["Custom query..."] + example_queries)
    
    if query == "Custom query...":
        query = st.text_input("Enter your query:")
    
    if st.button("Submit Query") and query:
        with st.spinner("Processing..."):
            # Process query through RAG
            response = rag_service.process_user_query(query)
        
        # Display response
        st.markdown("### Response:")
        st.markdown(response['response'])
        
        # Show metadata
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Confidence", f"{response['confidence']:.2%}")
        with col2:
            st.metric("Sources Used", len(response['sources']))
        
        # Show sources
        with st.expander("View Sources"):
            for source in response['sources']:
                st.markdown(f"**{source['title']}**")
                st.markdown(f"Type: {source['type']}")
                st.markdown(f"Relevance: {source.get('score', 'N/A')}")
                st.markdown("---")
        
        # Show suggestions
        if response['suggestions']:
            st.markdown("### 💡 Follow-up Questions:")
            for suggestion in response['suggestions']:
                st.markdown(f"- {suggestion}")

if __name__ == "__main__":
    main()
