import enum

class CartStatus(str, enum.Enum):
    InCart = 'InCart'
    Removed = 'Removed'
    Purchased = 'Purchased'
    CheckedOut = 'CheckedOut'


