import random


def generate_display_info() -> dict:
    """
    Generate display_info dengan nilai randomized:
    - rating: 4.7 - 5.0
    - sales_count: 10 - 70
    - discount_percentage: 5 - 30
    """
    return {
        "rating": round(random.uniform(4.7, 5.0), 1),
        "sales_count": random.randint(10, 70),
        "discount_percentage": random.randint(5, 30)
    }
