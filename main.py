from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Check if a number is perfect
def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

# Check if a number is an Armstrong number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Fetch a fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "No fun fact found."
    except:
        return "Could not retrieve fun fact."

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        # Convert input to integer
        num = int(number)

        # Analyze number properties
        prime = is_prime(num)
        perfect = is_perfect(num)
        armstrong = is_armstrong(num)
        digit_sum = sum(int(d) for d in str(num))
        parity = "odd" if num % 2 else "even"
        properties = ["armstrong", parity] if armstrong else [parity]

        # Get fun fact
        fun_fact = get_fun_fact(num)

        # Return JSON response
        return {
            "number": num,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
    except ValueError:
        return {"number": str(number), "error": True}
