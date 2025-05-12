import requests
import openai
import os
from openai import OpenAI


class LangChainService:
    def __init__(self, vector_db_repository):
        self.vector_db_repository = vector_db_repository
        # self.api_key = os.getenv("OPENAI_API_KEY")
        # openai.api_key = self.api_key
        self.ollama_url = "http://localhost:11434"  # Ollama's default API endpoint
        self.api_key = os.getenv("OLLAMA_API_KEY")

    def process_data(self, data):
        # Logic to process data using LangChain
        processed_data = self._langchain_process(data)
        return processed_data

    def generate_response(self, query):
        # Logic to generate a response based on the query
        response = self._langchain_generate(query)
        return response

    def _langchain_process(self, data):
        # Placeholder for LangChain processing logic
        return data  # Replace with actual processing logic

    def _langchain_generate(self, query):
        """
        Generate a response using Ollama's API.

        Args:
            query (str): The user's query.

        Returns:
            str: The generated response.
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {"model": "llama3.2", "prompt": query, "stream": False}
            print("Payload: ", payload)  # Debugging line
            print("Headers: ", headers)  # Debugging line
            print("Ollama URL: ", self.ollama_url)  # Debugging line
            response = requests.post(
                f"{self.ollama_url}/api/generate", json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json().get("response", "No response generated.")
        except Exception as e:
            print(f"Error generating response: {e}")
            return "An error occurred while generating the response."

    def _langchain_generate2(self, query):
        """
        Generate a response using OpenAI's ChatGPT model.

        Args:
            query (str): The user's query.

        Returns:
            str: The generated response.
        """
        try:
            client = OpenAI()

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can use "gpt-4" if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return "An error occurred while generating the response."
