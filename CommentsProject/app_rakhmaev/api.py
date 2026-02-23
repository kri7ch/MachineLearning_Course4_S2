import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from .db import fetch_comments, insert_comment
from .ml_model import ToxicCommentModel


class CommentIn(BaseModel):
    text: str


class CommentOut(BaseModel):
    id: int
    text: str
    is_toxic: int
    created_at: str | None


app = FastAPI(title="Toxic Comments API (Rakhmaev)")
model = ToxicCommentModel()


@app.get("/comments")
def get_comments():
    return fetch_comments()


@app.post("/comments")
def add_comment(payload: CommentIn):
    label = model.predict_label(payload.text)
    insert_comment(payload.text, label)
    return {"text": payload.text, "is_toxic": label}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
