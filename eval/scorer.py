import re
import json

PRICING = {
    "llama-3.1-70b-versatile": {"input": 0.0, "output": 0.0}, 
    "gpt-4o-mini":             {"input": 0.0, "output": 0.0},  
    "gemini-1.5-flash":        {"input": 0.0, "output": 0.0},  
    "llama3.1:8b":             {"input": 0.0, "output": 0.0},  
}

def score_hallucination(result):
    """
    Simple heuristic-based hallucination detection that doesn't require API calls.
    Checks if response contains key keywords from expected answer.
    """
    response_text = result['response'].lower()
    expected_text = result['expected'].lower()
    
    # Extract key words from expected answer (words > 3 chars, excluding common words)
    common_words = {'the', 'and', 'that', 'this', 'with', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'do', 'does', 'did', 'not', 'no', 'yes', 'but', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'a', 'an'}
    expected_words = set(word for word in expected_text.split() if len(word) > 3 and word not in common_words)
    
    if not expected_words:
        # If no key words, accept response as grounded
        return 1.0
    
    # Count how many key words from expected answer appear in response
    matched_words = sum(1 for word in expected_words if word in response_text)
    match_ratio = matched_words / len(expected_words)
    
    # If at least 50% of key words are present, consider it grounded
    return min(match_ratio, 1.0)
def score_accuracy(result):
    import re
    def normalize(text):
        return re.sub(r'\s+', ' ', text.strip().lower())
    return 1.0 if normalize(result['expected']) in normalize(result['response']) else 0.0
def score_tokens(result) -> dict :
    return {
        "input_tokens": result['input_tokens'],
        "output_tokens": result['output_tokens'],
        "total_tokens": result['input_tokens'] + result['output_tokens'],
    }
