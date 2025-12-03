COST_PER_1K_TOKENS_RUB = {
    "gpt-4o": 3.75,
    "gpt-4o-mini": 0.11,
    "claude-3-5-sonnet-20241022": 2.25,
    "gemini-1.5-flash": 0.26,
    "gigachat": 1.50,
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    price = COST_PER_1K_TOKENS_RUB.get(model, 2.0)
    total_tokens = input_tokens + output_tokens
    return round(total_tokens * price / 1000, 4)