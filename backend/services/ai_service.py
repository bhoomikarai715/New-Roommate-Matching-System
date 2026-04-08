import requests
import json
from backend.config import settings

def calculate_ai_compatibility(user_data: dict, candidate_data: dict) -> float:
    """
    Uses OpenRouter (Gemini/Gwen) to calculate compatibility score based on complex parameters.
    Returns a float between 50 and 100.
    """
    if not settings.OPENROUTER_API_KEY:
        # Fallback to 0 indicates we should use the traditional weighted matching
        return 0.0

    prompt = f"""
    Analyze the compatibility between two potential roommates based on their profiles.
    
    User 1 (The Searcher):
    {json.dumps(user_data, indent=2)}
    
    User 2 (The Candidate):
    {json.dumps(candidate_data, indent=2)}
    
    Consider sleep patterns, cleanliness, noise tolerance, and personality.
    Provide a compatibility score from 50 to 100, where 100 is a perfect match.
    Only return the numeric score.
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-001", # High quality, fast model
                "messages": [
                    {"role": "system", "content": "You are an expert roommate matching assistant. Return only a number."},
                    {"role": "user", "content": prompt}
                ]
            }),
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            score_text = result['choices'][0]['message']['content'].strip()
            # Extract just the numeric part if the model added fluff
            score = float(''.join(c for c in score_text if c.isdigit() or c == '.'))
            return max(50.0, min(100.0, score))
    except Exception as e:
        print(f"AI Compatibility calculation failed: {e}")
        
    return 0.0
