import json
import re

with open("app/products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def get_ai_response(message: str):

    message = message.lower().strip()
    

    buy_keywords = ["buy", "purchase", "how to pay", "payment", "checkout", "order"]
    if any(keyword in message for keyword in buy_keywords):
        product_name = message
        for keyword in buy_keywords:
            product_name = product_name.replace(keyword, "").strip()
            
        return {
            "text": "To complete your purchase, you can use Credit/Debit cards, PayPal, or Apple Pay/Google Pay. We offer secure, encrypted checkout. Once you select a product, just click 'Buy Now' on its card to proceed!",
            "products": [],
            "action": "payment_info"
        }


    greetings = ["hi", "hello", "hey", "start", "welcome"]
    if message in greetings or message == "":
        return {
            "text": "Hello! Welcome to our premium E-Commerce store. Are you looking for a new **phone**, **laptop**, **watch**, **tablet**, or **audio** device today?",
            "products": [],
            "action": "greet"
        }


    if "how are you" in message or "how r u" in message:
        return {
            "text": "I'm doing great, thanks for asking! 😊 I'm here and ready to help you find some amazing tech products. What's on your mind today?",
            "products": [],
            "action": "small_talk"
        }
    if "who are you" in message or "your name" in message:
        return {
            "text": "I'm your personal AI shopping assistant for SAM BOT Store! I can help you find the latest gadgets, compare specs, and even guide you through checkout.",
            "products": [],
            "action": "small_talk"
        }


    categories = ["phone", "laptop", "watch", "audio", "tablet"]
    for cat in categories:
        if cat in message:
            found_products = [p for p in PRODUCTS if p["category"] == cat][:5]
            if found_products:
                return {
                    "text": f"Awesome! Here are some of our top {cat}s. Which one catches your eye?",
                    "products": found_products,
                    "action": "show_products"
                }


    query = message.lower()
    query_words = set(query.split())
    
    exact_matches = []
    related_matches = []
    
    for p in PRODUCTS:
        name_lower = p["name"].lower()
        
        if query in name_lower:
            exact_matches.append(p)
        else:
            name_words = set(name_lower.split())
            match_count = len(query_words.intersection(name_words))
            if match_count > 0:
                related_matches.append((match_count, p))
                
    related_matches.sort(key=lambda x: x[0], reverse=True)
    related_products = [p[1] for p in related_matches][:5]

    if exact_matches:
        combined_results = exact_matches + [p for p in related_products if p not in exact_matches]
        return {
            "text": f"Here is what I found for '{message}':",
            "products": combined_results[:5],
            "action": "show_products"
        }
    elif related_products:
        return {
            "text": f"I couldn't find exactly '{message}', but here are the latest available options:",
            "products": related_products[:5],
            "action": "show_products"
        }


    return {
        "text": "I couldn't find exactly what you were looking for. Try searching for a specific brand or category like 'Samsung', 'iPhone', 'laptop', or 'headphones'!",
        "products": [],
        "action": "default"
    }
