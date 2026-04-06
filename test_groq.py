import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Groq initialization...")
print(f"GROQ_API_KEY set: {'GROQ_API_KEY' in os.environ}")

try:
    from groq import Groq
    print("✓ Groq imported")
    
    print("Attempting to create Groq client...")
    client = Groq()
    print("✓ Groq client created successfully!")
    
    print("Testing chat completion...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=10
    )
    print(f"✓ Chat completion successful: {response.choices[0].message.content[:50]}...")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
