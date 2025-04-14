import streamlit as st
import pandas as pd
import json
import io
from typing import Dict, List, Any
import os

# Import our modules
from ner_processor import NERProcessor
from utils import load_sample_texts, validate_pattern, format_pattern_for_display

# Set page configuration
st.set_page_config(
    page_title="Custom NER Application",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visualization
st.markdown("""
<style>
    .main {
        padding: 1rem 1rem;
    }
    .stTextInput > div > div > input {
        caret-color: #4CAF50;
    }
    .entity-table {
        font-size: 0.9rem;
    }
    .css-145kmo2 {
        font-size: 0.9rem;
    }
    .entity-label {
        font-weight: bold;
        padding: 0.2rem 0.5rem;
        border-radius: 0.5rem;
        white-space: nowrap;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'ner_processor' not in st.session_state:
    st.session_state.ner_processor = NERProcessor()

if 'entity_patterns' not in st.session_state:
    st.session_state.entity_patterns = {}  # {label: [patterns]}

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

if 'processed_doc' not in st.session_state:
    st.session_state.processed_doc = None

if 'show_help' not in st.session_state:
    st.session_state.show_help = False

# Functions for adding and removing patterns
def add_pattern():
    """Add a pattern to the entity label."""
    label = st.session_state.entity_label.strip()
    pattern = st.session_state.entity_pattern.strip()
    
    if not label:
        st.error("Entity label cannot be empty")
        return
    
    is_valid, error_msg, parsed_pattern = validate_pattern(pattern)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Add pattern to session state
    if label not in st.session_state.entity_patterns:
        st.session_state.entity_patterns[label] = []
    
    st.session_state.entity_patterns[label].append(parsed_pattern)
    
    # Clear the pattern input
    st.session_state.entity_pattern = ""

def remove_pattern(label, index):
    """Remove a pattern from the entity label."""
    if label in st.session_state.entity_patterns:
        if 0 <= index < len(st.session_state.entity_patterns[label]):
            st.session_state.entity_patterns[label].pop(index)
            
            # Remove label if no patterns remain
            if not st.session_state.entity_patterns[label]:
                del st.session_state.entity_patterns[label]

def process_text():
    """Process the input text with the NER processor."""
    # Get input text
    text = st.session_state.input_text.strip()
    
    if not text:
        st.error("Please enter some text to process")
        return
    
    # Reset the NER processor
    st.session_state.ner_processor.reset_custom_entities()
    
    # Add all patterns
    for label, patterns in st.session_state.entity_patterns.items():
        st.session_state.ner_processor.add_entity_patterns(label, patterns)
    
    # Process the text
    st.session_state.processed_doc = st.session_state.ner_processor.process_text(text)

def handle_file_upload():
    """Handle uploaded text file."""
    if st.session_state.uploaded_file is not None:
        text_file = st.session_state.uploaded_file
        
        # Read as string
        text_content = io.StringIO(text_file.getvalue().decode("utf-8")).read()
        
        # Set input text
        st.session_state.input_text = text_content

def load_sample_text():
    """Load selected sample text."""
    selected_sample = st.session_state.selected_sample
    
    if selected_sample and selected_sample != "None":
        sample_texts = load_sample_texts()
        if selected_sample in sample_texts:
            st.session_state.input_text = sample_texts[selected_sample]

def clear_all():
    """Clear all entity patterns and text."""
    st.session_state.entity_patterns = {}
    st.session_state.input_text = ""
    st.session_state.processed_doc = None
    st.session_state.ner_processor.reset_custom_entities()

def toggle_help():
    """Toggle help section visibility."""
    st.session_state.show_help = not st.session_state.show_help

# Application UI
st.title("🔍 Custom Named Entity Recognition")

# Main container
main_container = st.container()

with main_container:
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 Text Input", "🏷️ Entity Definition", "🔎 Results"])
    
    # Tab 1: Text Input
    with tab1:
        col1, col2 = st.columns([7, 3])
        
        with col1:
            st.text_area(
                "Enter text to process:",
                value=st.session_state.input_text,
                height=300,
                key="input_text"
            )
        
        with col2:
            st.file_uploader(
                "Or upload a text file:",
                type=["txt"],
                key="uploaded_file",
                on_change=handle_file_upload
            )
            
            sample_texts = load_sample_texts()
            sample_options = ["None"] + list(sample_texts.keys())
            
            st.selectbox(
                "Or select a sample text:",
                options=sample_options,
                key="selected_sample",
                on_change=load_sample_text
            )
            
            st.button("Clear All", on_click=clear_all)
    
    # Tab 2: Entity Definition
    with tab2:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Define Custom Entities")
            
            st.text_input(
                "Entity Label (e.g., PRODUCT, COMPANY):",
                key="entity_label"
            )
            
            st.text_area(
                "Entity Pattern:",
                key="entity_pattern",
                help="Simple text pattern (e.g., 'Microsoft') or token pattern as JSON array"
            )
            
            col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
            
            with col1_1:
                st.button("Add Pattern", on_click=add_pattern)
            
            with col1_3:
                st.button("Help", on_click=toggle_help)
            
            if st.session_state.show_help:
                with st.expander("Pattern Examples", expanded=True):
                    st.markdown("""
                    ### Simple Text Patterns
                    Just type the exact text to match: `Microsoft`
                    
                    ### Token Patterns (for advanced users)
                    Use JSON format to define specific token attributes:
                    ```json
                    [{"LOWER": "artificial"}, {"LOWER": "intelligence"}]
                    ```
                    
                    Common attributes:
                    - `LOWER`: Lowercase text
                    - `TEXT`: Exact text match
                    - `LEMMA`: Base form of word
                    - `POS`: Part of speech
                    - `IS_DIGIT`: True for numbers
                    
                    [Read more in the spaCy documentation](https://spacy.io/usage/rule-based-matching#entityruler)
                    """)
        
        with col2:
            st.subheader("Current Entity Patterns")
            
            if not st.session_state.entity_patterns:
                st.info("No entity patterns defined yet. Add some patterns first.")
            
            for label, patterns in st.session_state.entity_patterns.items():
                with st.expander(f"{label} ({len(patterns)} patterns)", expanded=True):
                    for i, pattern in enumerate(patterns):
                        col2_1, col2_2 = st.columns([5, 1])
                        
                        with col2_1:
                            st.code(format_pattern_for_display(pattern))
                        
                        with col2_2:
                            st.button(
                                "🗑️", 
                                key=f"remove_{label}_{i}",
                                on_click=remove_pattern,
                                args=(label, i)
                            )
    
    # Tab 3: Results
    with tab3:
        st.button("Process Text", on_click=process_text)
        
        if st.session_state.processed_doc is not None:
            doc = st.session_state.processed_doc
            entities = st.session_state.ner_processor.get_entities(doc)
            highlighted_html = st.session_state.ner_processor.get_highlighted_html(doc)
            
            # Display highlighted text
            st.subheader("Text with Highlighted Entities")
            st.markdown(highlighted_html, unsafe_allow_html=True)
            
            # Display entities table
            st.subheader("Detected Entities")
            
            if not entities:
                st.info("No entities detected. Try adding more patterns or different text.")
            else:
                entities_df = pd.DataFrame(entities)
                entities_df = entities_df[["text", "label", "start", "end"]]
                entities_df.columns = ["Text", "Label", "Start", "End"]
                st.dataframe(entities_df, use_container_width=True)
                
                # Entity count by label
                entity_counts = pd.DataFrame(entities).groupby("label").size().reset_index(name="count")
                entity_counts.columns = ["Label", "Count"]
                
                col3_1, col3_2 = st.columns([1, 1])
                
                with col3_1:
                    st.subheader("Entity Counts")
                    st.dataframe(entity_counts, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "Custom Named Entity Recognition App | Built with Streamlit and spaCy | "
    "[GitHub Repository](https://github.com/Emanuel-TellesChaves/NERStreamlitApp)"
)

# Run once at startup to download the model
if 'model_downloaded' not in st.session_state:
    with st.spinner('Downloading spaCy model (first run only)...'):
        # This will download the model if not already installed
        _ = NERProcessor()
    st.session_state.model_downloaded = True 