from sqlalchemy import create_engine # type: ignore

# Banco local SQLite
engine = create_engine("sqlite:///trading.db")
