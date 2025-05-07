from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Model dla danych wejściowych
class InputData(BaseModel):
    input: str

# Model dla danych wyjściowych
class OutputData(BaseModel):
    output: str

@app.post("/webhook")
async def webhook(data: InputData):
    # Odbieramy dane z pola "input" i zwracamy to samo w polu "output"
    return OutputData(output=data.input)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
