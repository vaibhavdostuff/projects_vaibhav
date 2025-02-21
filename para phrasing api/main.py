
import requests

def paraphrase_with_huggingface(text, api_key):
    """Paraphrase the given text using Hugging Face Inference API."""
    
    # Using the t5-base model

    url = "https://api-inference.huggingface.co/models/t5-base"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Payload for generating paraphrased sentences
    payload = {
        "inputs": f"paraphrase: {text}",
        "parameters": {
            "num_return_sequences": 3,  # Requesting 3 paraphrases
            "max_length": 50,
            "temperature": 1.5
            }
    }

    response = requests.post(url, headers=headers, json=payload)

    # Handling the API response

    if response.status_code == 200:
        paraphrased_text = response.json()
        # Check if 'translation_text' is in the response and return that
        if 'translation_text' in paraphrased_text[0]:
            return [item['translation_text'] for item in paraphrased_text]
        

# Example usage

api_key = "your Hugging Face API key"  # Replace with your Hugging Face API key
input_sentence = "I will see you there."

try:

    paraphrased_sentences = paraphrase_with_huggingface(input_sentence, api_key)
    print("Original Sentence:", input_sentence)
    print("Paraphrased Sentences:")
    
    
    # Displaying the paraphrased sentences
    
    for i, sentence in enumerate(paraphrased_sentences, 1):
        print(f"{i}: {sentence.strip()}")
except Exception as e:
    print(e)

