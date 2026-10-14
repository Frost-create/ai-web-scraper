import os
import requests
from google import genai

def fetch_webpage_text(url):
    """Fetches the raw text content of a webpage."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # We use response.text to get the raw HTML/text string
        return response.text[:8000] # Limit characters so we don't overload the API
    except Exception as e:
        return f"Error fetching URL: {e}"

def summarize_with_ai(raw_text):
    """Sends the scraped text to Gemini AI for a clean summary."""
    # The client automatically looks for the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    prompt = f"Extract the main news or core article content from this raw webpage data and summarize it into 3 punchy bullet points:\n\n{raw_text}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Generation Error: {e}"

def main():
    print("--- AI Web Scraper & Summarizer ---")
    target_url = input("Enter a URL to scrape and summarize: ")
    
    print("\nFetching webpage data...")
    web_text = fetch_webpage_text(target_url)
    
    print("Sending data to AI for analysis...")
    summary = summarize_with_ai(web_text)
    
    print("\n=== AI SUMMARY ===")
    print(summary)

if __name__ == "__main__":
    main()
