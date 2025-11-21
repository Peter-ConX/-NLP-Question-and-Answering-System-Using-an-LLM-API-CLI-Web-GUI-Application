import os
import re
import string
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return " ".join(tokens)

def get_llm_response(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer concisely and accurately."},
            {"role": "user", "content": question}
        ],
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=1024
    )
    return chat_completion.choices[0].message.content

def main():
    print("=== LLM Q&A System (CLI) ===")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("Ask your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        if not question:
            print("Please enter a valid question.\n")
            continue
        
        print("Original :", question)
        
        processed = preprocess_text(question)
        print("Processed:", processed)
        
        print("\nGenerating answer from LLM...\n")
        
        try:
            answer = get_llm_response(processed)
            print("Answer:")
            print(answer)
            print("\n" + "-"*50 + "\n")
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure your GROQ_API_KEY is set in .env file.\n")

if __name__ == "__main__":
    main()