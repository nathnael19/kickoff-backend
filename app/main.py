from fastapi import FastAPI


app = FastAPI(title="Kick OFF")


@app.get("/")
def home():
    return {"message": "homepage"}
