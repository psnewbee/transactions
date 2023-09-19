import enum


class TransactionTypesEnum(enum.Enum):
    income: str = "income"
    outcome: str = "outcome"


class TransactionStatusEnum(enum.Enum):
    successful: str = "Successful: transaction approved"
    unsuccessful: str = "Iterrupted: insufficient funds"
