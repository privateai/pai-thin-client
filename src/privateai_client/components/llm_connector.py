import os
from typing import Dict, List, Union

class LLMConnector:

    accepted_llms = ["openai", "cohere", "palm", "vertexai"]
        
    def _vertexai_prompt_completion(self, prompt:str, chat_model_name:str, project:str=None, location:str = None, **kwargs):
        import vertexai
        from vertexai.preview.language_models import ChatModel

        vertexai.init(project=project, location=location)
        chat_model = ChatModel.from_pretrained(chat_model_name)
        chat_parameters = kwargs
        chat = chat_model.start_chat(**kwargs)
        completion = chat.send_message(f'{prompt}', chat_parameters)
        return completion.text
    
    def _cohere_prompt_completion(self, prompt:str, **kwargs):
        import cohere
        if kwargs.get("model_api_key"):
            model_api_key = kwargs.pop("model_api_key")
        elif os.getenv["model_api_key"]:
            model_api_key = os.getenv["model_api_key"]
        cohere_llm = cohere.Client(api_key=model_api_key, **kwargs)
        response = cohere_llm.generate(
            prompt=prompt,
            **kwargs)
        return [prompt, response.generations[0].text]

    def _openai_prompt_completion(self, prompt:Union[str, List[Dict[str,str]]], **kwargs):
        import openai
        model_api_key = None
        if kwargs.get("model_api_key"):
            model_api_key = kwargs.pop("model_api_key")
        if type(prompt) == str:
            prompt = [
                {"role": "user",
                "content": prompt},
            ]

        openai.api_key = model_api_key
        completion = openai.ChatCompletion.create(
        messages=prompt,
        **kwargs
        )
        prompt = [prompt[0]["content"], completion.choices[0].message["content"]]
        return prompt

    def send_redacted_prompt(self, prompt, llm_model: str, **kwargs):
        if llm_model.lower() in self.accepted_llms:
            if llm_model.lower() == "openai":
                return self._openai_prompt_completion(prompt, **kwargs)
            elif llm_model.lower() == "cohere":
                return self._cohere_prompt_completion(prompt, **kwargs)
            elif llm_model.lower() == "palm" or llm_model.lower() == "vertexai":
                return self._vertexai_prompt_completion(prompt, **kwargs)
        else:
             raise ValueError(f"{llm_model} is not an accepted LLM. Accepted LLMs are {self.accepted_llms}")

