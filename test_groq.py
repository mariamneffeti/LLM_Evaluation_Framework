import os
from groq import Groq

def test_groq_connection():
    assert "GROQ_API_KEY" in os.environ, "GROQ_API_KEY not found in environment"
    
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    
    assert response.choices[0].message.content is not None
    print(f"✓ Chat completion successful")