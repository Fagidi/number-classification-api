from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

# Function to check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)

# Function to get a fun fact from the Numbers API
def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "No fun fact found."
    except:
        return "Could not retrieve fun fact."

# API Endpoint to Classify a Number
@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    # If input is not an integer, return HTTP 400
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail={"number": str(number), "error": True})

    # Compute number properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    digit_sum = sum(int(d) for d in str(abs(number)))  # Handle negatives properly
    parity = "odd" if number % 2 else "even"
    properties = ["armstrong", parity] if armstrong else [parity]

    #Fetch fun fact
    fun_fact = get_fun_fact(number)

    return {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
