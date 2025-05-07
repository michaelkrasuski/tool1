from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class InputData(BaseModel):
    input: str

class OutputData(BaseModel):
    output: str

BADANIA_URL = "https://letsplay.ag3nts.org/data/badania.json?v=1743591162"

@app.post("/webhook")
async def webhook(data: InputData):
    if data.input.startswith("test"):
        return OutputData(output=data.input)
    if data.input == "pobierz badania o podrozach w czasie":
        try:
            response = requests.get(BADANIA_URL)
            response.raise_for_status()
            badania = response.json()
            for badanie in badania:
                if "podróże w czasie" in badanie["nazwa"].lower():
                    result = {
                        "nazwa": badanie["nazwa"],
                        "uczelnia": badanie["uczelnia"],
                        "sponsor": badanie["sponsor"]
                    }
                    return OutputData(output=json.dumps(result, ensure_ascii=False))
            return OutputData(output="Nie znaleziono badania")
        except requests.RequestException as e:
            return OutputData(output=f"Błąd: {str(e)}")
    return OutputData(output="Nieprawidłowe zapytanie")
