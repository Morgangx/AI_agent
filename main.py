import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse, GenerateContentResponseUsageMetadata
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main() -> None:
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found")
    client: genai.Client = genai.Client(api_key=api_key)
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Chatbot")
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
        print(f"User prompt: {parser}")
        print(f"Prompt tokens: {usage_metadada.prompt_token_count}")
        print(f"Response tokens: {usage_metadada.candidates_token_count}")
        
    print("Response:")
    if function_calls is None:
        print(response.text)
    else:
        function_results: list[types.Part] = []
        for function_call in function_calls:
            func_result: types.Content = call_function(function_call)
            if not func_result.parts:
                raise Exception("Function result parts don't exist")
            func_response: types.FunctionResponse = func_result.parts[0].function_response # type: ignore
            if not func_response:
                raise Exception("FuntionResponse object doesn't exist")
            if not func_response.response:
                raise Exception("No response from the function call")
            function_results.append(func_result.parts[0])
            if args.verbose:
                print(f"-> {func_result.parts[0].function_response.response}") # type: ignore

if __name__ == "__main__":
    main()
