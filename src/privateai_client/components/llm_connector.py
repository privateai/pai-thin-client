import openai
import cohere
import vertexai
from vertexai.preview.language_models import ChatModel

class CohereConnector:
    def __init__(self, model_api_key: str, **kwargs):
        self.cohere = cohere.Client(model_api_key, **kwargs)
    
    def prompt_completion(self, text, **kwargs):
        response = self.cohere.generate(
            prompt=text,
            **kwargs)
        return response.generations[0].text

class OpenAIConnector:
    def __init__(self, model_api_key: str):
        openai.api_key = model_api_key
    
    def prompt_completion(self, text, **kwargs):
        completion = openai.ChatCompletion.create(
        messages=[
        {"role": "user",
         "content": text},
        ],
        **kwargs
        )
        return completion.choices[0].message['content']

class VertexAIConnector:
    def __init__(self, project: str, location: str, chat_model_name: str, **kwargs):
        project = kwargs.pop("project")
        location = kwargs.pop("location")
        chat_model_name = kwargs("chat_model_name")

        vertexai.init(project=project, location=location)
        self.chat_model = ChatModel.from_pretrained(chat_model_name)
        self.chat_parameters = kwargs

    def prompt_completion(self, text, **kwargs):
        chat = self.chat_model.start_chat(context=kwargs.pop(kwargs["context"]), **kwargs)
        completion = chat.send_message(f'{text}', **self.chat_parameters)
        return completion.text

class LLMConnector:

    accepted_llms = ["openai", "cohere", "palm", "vertexai"]

    def __init__(self, model_name: str, model_api_key: str, **kwargs):
        if model_name.lower() in self.accepted_llms:
            if model_name.lower() == "openai":
                self.llm = OpenAIConnector(model_api_key=model_api_key)
            elif model_name.lower() == "cohere":
                self.llm = CohereConnector(model_api_key=model_api_key, **kwargs)
            elif model_name.lower() == "palm" or model_name.lower() == "vertexai":
                self.llm = VertexAIConnector(model_api_key=model_api_key, **kwargs)


        else:
             raise ValueError(f"{model_name} is not an accepted LLM. Accepted LLMs are {self.accepted_llms}")

    def send_redacted_prompt(self, text: str, **kwargs):
        return self.llm.prompt_completion(text, **kwargs)

