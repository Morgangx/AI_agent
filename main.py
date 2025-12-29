import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse, GenerateContentResponseUsageMetadata
from prompts import system_prompt
from functions.call_function import available_functions

def main() -> None:
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found")
    client: genai.Client = genai.Client(api_key=api_key)
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Chatbot")
    prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args: argparse.Namespace = parser.parse_args()
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response: GenerateContentResponse = client.models.generate_content( # type: ignore
        model="gemini-2.5-flash",
        contents=messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

    usage_metadada: GenerateContentResponseUsageMetadata | None = response.usage_metadata
    if usage_metadada == None:
        raise RuntimeError("No usage metadata found!")
    
    function_calls: list[types.FunctionCall] | None = response.function_calls

    if args.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage_metadada.prompt_token_count}")
        print(f"Response tokens: {usage_metadada.candidates_token_count}")
        
    print("Response:")
    if function_calls is None:
        print(response.text)
    else:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()
