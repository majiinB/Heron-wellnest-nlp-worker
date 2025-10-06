from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import torch

class NLPService:
    def __init__(self, model_path: str, id_to_label: dict = None):
        """
        Initialize the NLP service with model and tokenizer.
        Optionally accepts an id_to_label mapping for readable output.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.id_to_label = id_to_label or {}  # fallback to numeric IDs if not provided

    def analyze_text(self, text, top_k: int = None):
        """
        Analyze text(s) and return label probabilities in a readable dict format.

        Args:
            text (str or list[str]): One or multiple texts.
            top_k (int, optional): If set, returns only the top_k most probable labels.

        Returns:
            dict or list[dict]: Label-probability map(s).
        """
        single_input = False
        if isinstance(text, str):
            text = [text]
            single_input = True

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)

        probs = probs.cpu()
        results = []

        for example_probs in probs:
            probs_list = example_probs.tolist()
            label_percent = {
                self.id_to_label.get(i, str(i)): round(p * 100.0, 2)
                for i, p in enumerate(probs_list)
            }

            sorted_labels = sorted(label_percent.items(), key=lambda x: x[1], reverse=True)

            if top_k is not None:
                sorted_labels = sorted_labels[:top_k]
                label_percent = dict(sorted_labels)

            results.append(label_percent)

        return results[0] if single_input else results