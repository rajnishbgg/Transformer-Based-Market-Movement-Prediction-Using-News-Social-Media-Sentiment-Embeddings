# from transformers import pipeline

# class SentimentAnalyzer:

#     def __init__(self):
#         print("Loading FinBERT model...")
#         self.classifier = pipeline(
#             "sentiment-analysis",
#             model="ProsusAI/finbert"
#         )

#     def get_sentiment_score(self, text):

#         result = self.classifier(text)[0]
#         label = result["label"]

#         if label.lower() == "positive":
#             return 1
#         elif label.lower() == "negative":
#             return -1
#         else:
#             return 0

from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        print("Loading FinBERT model...")
        self.classifier = pipeline(
            "sentiment-analysis",
            model="ProsusAI/finbert"
        )

    def analyze(self, text):
        result = self.classifier(text)[0]

        label = result["label"]
        confidence = round(result["score"] * 100, 2)

        if label == "positive":
            market = "Bullish 📈"
        elif label == "negative":
            market = "Bearish 📉"
        else:
            market = "Neutral ➖"

        return {
            "sentiment": label.capitalize(),
            "confidence": confidence,
            "market": market
        }