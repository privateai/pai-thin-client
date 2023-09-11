from src.privateai_client.components import request_objects
import src.privateai_client.pai_client

print("test")
pai_client = src.privateai_client.pai_client.PAIClient(url="http://localhost:8080")

# llm_response = pai_client.send_redacted_prompt(prompt="My sample name is John Smith", llm_model="openai", model="gpt-3.5-turbo", model_api_key="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")

# llm_response = pai_client.send_redacted_prompt(prompt="My sample name is John Smith", llm_model="cohere", model_api_key="cEny3GlMvxLlv3wq1cILUGbDzbJ6dAwMZzL8nc17")
print("end test")
