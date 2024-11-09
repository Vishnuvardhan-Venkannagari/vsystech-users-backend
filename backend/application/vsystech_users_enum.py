import enum

class CartStatus(str, enum.Enum):
    InCart = 'InCart'
    Removed = 'Removed'
    Purchased = 'Purchased'
    CheckedOut = 'CheckedOut'


class PaymentStatus(str, enum.Enum):
    PAID = 'PAID'
    CANCELED = 'CANCELED'
    CHECKEDOUT = 'CHECKEDOUT'
    Authorized = 'Authorized'
    Captured = 'Captured'
    Refunded = 'Refunded'
    Failed = 'Failed'
    Pending = 'Pending'