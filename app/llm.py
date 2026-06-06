from llama_cpp import Llama

class LLM:
    def __init__(self):
        self.llm = Llama(
            model_path="data/models/TheBloke/tinyllama-1.1b-chat-v1.0.Q8_0.gguf",  # 🔥 put model here
            n_ctx=2048,
            n_threads=4  # adjust to your CPU cores
        )

    def generate(self, prompt):
        output = self.llm(
            prompt,
            max_tokens=200,
            temperature=0.2
        )

        return output["choices"][0]["text"]