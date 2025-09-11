import json
import re

# Load the JSON with abstracts
with open('AIB_presentation_list_with_abstracts.json', 'r') as f:
    presentations = json.load(f)

def clean_abstract(abstract, title, authors):
    """Clean abstract by removing references, title, and author names"""
    if not abstract:
        return ""
    
    # Original abstract for fallback
    original = abstract
    
    # Remove reference sections
    # Look for common reference section markers
    reference_patterns = [
        r'(?i)\n\s*REFERENCES?\s*\n.*',  # REFERENCES or REFERENCE followed by content
        r'(?i)\n\s*REFERENCE\s+LIST\s*\n.*',  # REFERENCE LIST
        r'(?i)\n\s*Bibliography\s*\n.*',  # Bibliography
        r'(?i)\n\s*Works?\s+Cited\s*\n.*',  # Works Cited
        r'(?i)\n\s*Literature\s+Cited\s*\n.*',  # Literature Cited
    ]
    
    for pattern in reference_patterns:
        abstract = re.sub(pattern, '', abstract, flags=re.DOTALL)
    
    # Also look for references by citation pattern (e.g., Author, Y. (2020). Title...)
    # This pattern looks for typical academic citation format
    citation_pattern = r'\n\s*[A-Z][a-zA-Z\-]+,\s+[A-Z]\.\s*(?:\([0-9]{4}\)|\d{4})\..*(?:\n\s*[A-Z][a-zA-Z\-]+,\s+[A-Z]\.\s*(?:\([0-9]{4}\)|\d{4})\..*)*$'
    abstract = re.sub(citation_pattern, '', abstract, flags=re.MULTILINE)
    
    # Find where references likely start based on multiple citations in sequence
    # Look for patterns like multiple lines starting with author names and years
    lines = abstract.split('\n')
    ref_start_idx = -1
    consecutive_citations = 0
    
    for i, line in enumerate(lines):
        # Check if line looks like a citation
        if re.match(r'^\s*[A-Z][a-zA-Z\-]+,\s+[A-Z]\..*\(?\d{4}\)?', line.strip()):
            consecutive_citations += 1
            if consecutive_citations >= 2 and ref_start_idx == -1:
                ref_start_idx = i - 1  # Start from the line before the first citation
        else:
            consecutive_citations = 0
    
    if ref_start_idx > 0:
        # Check if there's a REFERENCES header nearby
        for j in range(max(0, ref_start_idx - 3), ref_start_idx + 1):
            if j < len(lines) and re.match(r'(?i)^\s*(REFERENCES?|REFERENCE\s+LIST|Bibliography|Works?\s+Cited)', lines[j]):
                abstract = '\n'.join(lines[:j])
                break
        else:
            abstract = '\n'.join(lines[:ref_start_idx])
    
    # Remove title if it appears at the beginning
    if title:
        # Escape special regex characters in title
        escaped_title = re.escape(title)
        # Remove title from beginning (case insensitive)
        abstract = re.sub(f'^\\s*{escaped_title}\\s*', '', abstract, flags=re.IGNORECASE)
        # Also try removing title that might be split across lines
        title_words = title.split()
        if len(title_words) > 3:
            # Try to match title even if it's wrapped
            title_pattern = '\\s*'.join(re.escape(word) for word in title_words)
            abstract = re.sub(f'^\\s*{title_pattern}\\s*', '', abstract, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove author names
    if authors:
        for author in authors:
            if 'name' in author:
                name = author['name']
                # Split name into parts
                name_parts = name.split()
                
                # Remove full name
                escaped_name = re.escape(name)
                abstract = re.sub(f'\\b{escaped_name}\\b', '', abstract, flags=re.IGNORECASE)
                
                # Remove last name only (common in abstracts)
                if len(name_parts) > 1:
                    last_name = name_parts[-1]
                    # Only remove if it's followed by typical citation patterns or at the beginning
                    abstract = re.sub(f'^\\s*{re.escape(last_name)}\\b', '', abstract, flags=re.IGNORECASE | re.MULTILINE)
                    abstract = re.sub(f'\\b{re.escape(last_name)}\\s*\\(\\d{{4}}\\)', '', abstract, flags=re.IGNORECASE)
                
                # Remove first name only
                if len(name_parts) > 0:
                    first_name = name_parts[0]
                    abstract = re.sub(f'^\\s*{re.escape(first_name)}\\b', '', abstract, flags=re.IGNORECASE | re.MULTILINE)
    
    # Clean up author affiliations that might appear at the beginning
    # Pattern for affiliations (e.g., "University of...", "Department of...")
    affiliation_pattern = r'^(?:\s*(?:\d+\s*)?(?:University|Department|School|College|Institute|Center|Faculty)\s+of\s+[^\n]+\n?)+'
    abstract = re.sub(affiliation_pattern, '', abstract, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    abstract = re.sub(email_pattern, '', abstract)
    
    # Remove common header/footer elements
    abstract = re.sub(r'(?i)^\s*Abstract\s*:?\s*', '', abstract)  # Remove "Abstract:" header
    abstract = re.sub(r'(?i)^\s*Summary\s*:?\s*', '', abstract)  # Remove "Summary:" header
    abstract = re.sub(r'(?i)^\s*Keywords?\s*:.*$', '', abstract, flags=re.MULTILINE)  # Remove keywords line
    abstract = re.sub(r'(?i)^\s*JEL\s+(?:Classification|Codes?)\s*:.*$', '', abstract, flags=re.MULTILINE)  # Remove JEL codes
    
    # Remove page numbers and headers/footers
    abstract = re.sub(r'^\s*\d+\s*$', '', abstract, flags=re.MULTILINE)  # Page numbers
    abstract = re.sub(r'^\s*Page\s+\d+.*$', '', abstract, flags=re.MULTILINE | re.IGNORECASE)
    
    # Clean up extra whitespace
    abstract = re.sub(r'\n\s*\n\s*\n+', '\n\n', abstract)  # Multiple blank lines to double
    abstract = re.sub(r'^\s+|\s+$', '', abstract)  # Trim leading/trailing whitespace
    abstract = re.sub(r' +', ' ', abstract)  # Multiple spaces to single
    
    # If we removed too much (abstract is now very short), return original
    if len(abstract) < 100 and len(original) > 200:
        return original
    
    return abstract

# Clean all abstracts
cleaned_count = 0
for presentation in presentations:
    if presentation.get('abstract'):
        original_length = len(presentation['abstract'])
        presentation['abstract'] = clean_abstract(
            presentation['abstract'],
            presentation.get('title', ''),
            presentation.get('authors', [])
        )
        new_length = len(presentation['abstract'])
        if new_length < original_length:
            cleaned_count += 1
            print(f"Cleaned abstract for: {presentation.get('title', 'Unknown')[:50]}...")
            print(f"  Reduced from {original_length} to {new_length} characters")

print(f"\nTotal abstracts cleaned: {cleaned_count}")

# Save the cleaned JSON
with open('AIB_presentation_list_cleaned_abstracts.json', 'w') as f:
    json.dump(presentations, f, indent=2)

print(f"Saved cleaned abstracts to AIB_presentation_list_cleaned_abstracts.json")