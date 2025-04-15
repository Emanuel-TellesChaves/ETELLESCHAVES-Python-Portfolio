# Monkey patch for typing.TypeVar issue
import sys
import typing
if not hasattr(typing.TypeVar, '__class_getitem__'):
    # Add the method to make TypeVar compatible with subscripting
    def _class_getitem(cls, key):
        return cls
    typing.TypeVar.__class_getitem__ = classmethod(_class_getitem)

import spacy
from spacy.tokens import Doc, Span
from spacy.language import Language
from typing import Dict, List, Tuple, Any
import json
from utils import get_color_for_label

class NERProcessor:
    """Class for handling Named Entity Recognition processing using spaCy."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the NER processor with a spaCy model.
        
        Args:
            model_name (str): Name of the spaCy model to use
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            # If model isn't installed, download it
            try:
                spacy.cli.download(model_name)
                self.nlp = spacy.load(model_name)
            except Exception as e:
                # Fallback to loading from the full path
                import en_core_web_sm
                self.nlp = en_core_web_sm.load()
        
        # Remove the existing entity ruler if present
        if "entity_ruler" in self.nlp.pipe_names:
            self.nlp.remove_pipe("entity_ruler")
        
        # Add a new entity ruler with higher priority to override existing entities
        self.ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        self.ruler.overwrite_ents = True  # Ensure custom entities override existing ones
        
        # Store custom entity definitions
        self.custom_entities = {}
    
    def add_entity_patterns(self, label: str, patterns: List[Any]):
        """
        Add entity patterns to the entity ruler.
        
        Args:
            label (str): Entity label
            patterns (List[Any]): List of patterns (strings or dicts)
        """
        pattern_list = []
        
        for pattern in patterns:
            if isinstance(pattern, str):
                # Simple string pattern
                pattern_list.append({"label": label, "pattern": pattern})
            else:
                # Dict pattern with token attributes
                pattern_list.append({"label": label, "pattern": pattern})
        
        # Add patterns to the ruler
        self.ruler.add_patterns(pattern_list)
        
        # Store in custom entities
        if label not in self.custom_entities:
            self.custom_entities[label] = []
        self.custom_entities[label].extend(patterns)
    
    def process_text(self, text: str) -> Doc:
        """
        Process text with the spaCy pipeline.
        
        Args:
            text (str): Input text to process
            
        Returns:
            Doc: spaCy Doc object with entities
        """
        if not text.strip():
            # Return empty doc if text is empty
            return self.nlp("")
        
        return self.nlp(text)
    
    def get_entities(self, doc: Doc) -> List[Dict[str, Any]]:
        """
        Extract entities from a processed document.
        
        Args:
            doc (Doc): Processed spaCy Doc
            
        Returns:
            List[Dict[str, Any]]: List of entity dictionaries
        """
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_,
                "color": get_color_for_label(ent.label_)
            })
        return entities
    
    def get_highlighted_html(self, doc: Doc) -> str:
        """
        Generate HTML with highlighted entities.
        
        Args:
            doc (Doc): Processed spaCy Doc
            
        Returns:
            str: HTML string with highlighted entities
        """
        if not doc.ents:
            return doc.text
        
        html = ""
        last_end = 0
        
        for ent in doc.ents:
            # Add text between entities
            html += doc.text[last_end:ent.start_char]
            
            # Add highlighted entity
            color = get_color_for_label(ent.label_)
            html += f'<mark style="background-color: {color}; border-radius: 4px; padding: 0.15em 0.3em; margin: 0 0.1em; line-height: 1.5;">{ent.text}<span style="font-size: 0.7em; font-weight: bold; line-height: 1; vertical-align: super; margin-left: 0.3em">{ent.label_}</span></mark>'
            
            last_end = ent.end_char
            
        # Add any remaining text
        html += doc.text[last_end:]
        
        return html
    
    def reset_custom_entities(self):
        """Reset all custom entity patterns."""
        if "entity_ruler" in self.nlp.pipe_names:
            self.nlp.remove_pipe("entity_ruler")
        
        # Add a new entity ruler with higher priority
        self.ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        self.ruler.overwrite_ents = True  # Ensure custom entities override existing ones
        self.custom_entities = {}
    
    def get_custom_entities(self) -> Dict[str, List[Any]]:
        """
        Get the current custom entity definitions.
        
        Returns:
            Dict[str, List[Any]]: Dictionary of entity labels and their patterns
        """
        return self.custom_entities 