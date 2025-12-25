import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse, GenerateContentResponseUsageMetadata

def main() -> None:
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found")
    client: genai.Client = genai.Client(api_key=api_key)
    prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response: GenerateContentResponse = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    usage_metadada: GenerateContentResponseUsageMetadata | None = response.usage_metadata
    if usage_metadada == None:
        raise RuntimeError("No usage metadata found!")
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {usage_metadada.prompt_token_count}")
    print(f"Response tokens: {usage_metadada.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
