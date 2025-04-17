import os 
import sys

import openai 
from openai import OpenAI
from typing import Optional, Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

class LLMService: 
    """Class for interacting with the language models
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.client = OpenAI(
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY
        )
        
        
    def get_completions(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = settings.OPENROUTER_MODEL_NAME,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 500
    ) -> Dict[str, Any]:
        """Get completions from the language model.

        Args:
            messages (List[Dict[str, str]]): List of messages to send to the model.
            model (Optional[str], optional): Model name. Defaults to settings.OPENROUTER_MODEL_NAME.
            temperature (Optional[float], optional): Sampling temperature. Defaults to 0.7.
            max_tokens (Optional[int], optional): Maximum number of tokens to generate. Defaults to 500.

        Returns:
            Dict[str, Any]: Response from the model.
        """
        try: 
            response = self.client.chat.completions.create(
                extra_headers={}, 
                extra_body={},
                model=model,
                messages=messages, 
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in get_completions: {e}")
            return {"error": str(e)}
        
# test this method 
if __name__ == "__main__":
    llm_service = LLMService()
    messages = [
        {"role": "user", "content": "what is your name?"}
    ]
    response = llm_service.get_completions(messages)
    print(response)