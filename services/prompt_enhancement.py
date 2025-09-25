from typing import Dict, Any, Optional
import requests
import json

def enhance_prompt(
    api_key: str,
    prompt: str,
    **kwargs
) -> str:

    url = "https://engine.prod.bria-api.com/v1/prompt_enhancer"

    headers = {
        'api_token': api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': prompt,
        **kwargs
    }

    #for error handling and debugging
    try:
        print(f"Making request to: {url}")
        print(f"With headers: {headers}")
        print(f"With data: {data}")
        
        '''requests.post() → Bria API ko POST request bhej raha hai, saath me headers aur data.
        raise_for_status() → agar koi error aaya (404, 500) to exception throw karega.'''
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        result = response.json()
        return result.get("prompt variations", prompt)  # Return original prompt if enhancement fails
    except Exception as e:
        print(f"Error enhancing prompt: {e}")
        return prompt  # return original prompt on error
    
