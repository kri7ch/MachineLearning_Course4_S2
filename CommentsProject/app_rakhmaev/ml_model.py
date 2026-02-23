import numpy as np
from pathlib import Path
from pickle import load

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "comment_tone_rakhmaev_model.h5"
TOKENIZER_PATH = BASE_DIR / "comment_tone_rakhmaev_tokenizer.pkl"
MAX_LEN = 300


class ToxicCommentModel:
    def __init__(self):
        self.model = load_model(MODEL_PATH)
        with open(TOKENIZER_PATH, "rb") as f:
            self.tokenizer = load(f)

    def predict_proba(self, text: str) -> float:
        seq = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=MAX_LEN)
        proba = self.model.predict(padded, verbose=0).ravel()[0]
        return float(proba)

    def predict_label(self, text: str, threshold: float = 0.5) -> int:
        proba = self.predict_proba(text)
        return int(proba >= threshold)

