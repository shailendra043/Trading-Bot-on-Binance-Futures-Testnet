def round_to_precision(value: float, precision: int) -> float:
    return round(value, precision)
import re
from typing import Any

class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> None:
    if not re.match(r'^[A-Z0-9]{6,}$', symbol):
        raise ValidationError(f"Invalid symbol format: {symbol}")

def validate_side(side: str) -> None:
    if side.upper() not in ("BUY", "SELL"):
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL.")

def validate_quantity(quantity: Any) -> None:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValidationError("Quantity must be positive.")
    except Exception:
        raise ValidationError(f"Invalid quantity: {quantity}")

def validate_price(price: Any) -> None:
    try:
        p = float(price)
        if p <= 0:
            raise ValidationError("Price must be positive.")
    except Exception:
        raise ValidationError(f"Invalid price: {price}")

def validate_order_type(order_type: str) -> None:
    valid_types = ["MARKET", "LIMIT", "STOP_LIMIT", "OCO", "TWAP", "GRID"]
    if order_type.upper() not in valid_types:
        raise ValidationError(f"Invalid order type: {order_type}")
