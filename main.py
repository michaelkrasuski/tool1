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
UCZELNIE_URL = "https://letsplay.ag3nts.org/data/uczelnie.json?v=1743591162"

@app.post("/webhook")
async def webhook(data: InputData):
    if data.input.startswith("test"):
        return OutputData(output=data.input)
    if data.input == "pobierz badania o podrozach w czasie":
        try:
            # Pobierz dane z badania.json
            response_badania = requests.get(BADANIA_URL)
            response_badania.raise_for_status()
            badania = response_badania.json()
            
            # Pobierz dane z uczelnie.json
            response_uczelnie = requests.get(UCZELNIE_URL)
            response_uczelnie.raise_for_status()
            uczelnie = response_uczelnie.json()
            
            # Znajdź badanie o podróżach w czasie
            for badanie in badania:
                if "podróże w czasie" in badanie["nazwa"].lower():
                    uczelnia_id = badanie["uczelnia"]  # ID uczelni z badania.json
                    # Znajdź uczelnię po ID
                    for uczelnia in uczelnie:
                        if uczelnia["id"] == uczelnia_id:
                            result = {
                                "nazwa": badanie["nazwa"],
                                "uczelnia": uczelnia["nazwa"],  # Pełna nazwa uczelni
                                "sponsor": badanie["sponsor"]
                            }
                            return OutputData(output=json.dumps(result, ensure_ascii=False))
                    return OutputData(output="Nie znaleziono uczelni dla ID")
            return OutputData(output="Nie znaleziono badania")
        except requests.RequestException as e:
            return OutputData(output=f"Błąd: {str(e)}")
    return OutputData(output="Nieprawidłowe zapytanie")
