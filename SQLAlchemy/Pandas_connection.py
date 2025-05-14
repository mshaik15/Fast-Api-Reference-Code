from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd

# Load secret
load_dotenv("secrets.env")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Create engine
engine = create_engine(
    f'postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/sqltutorial',
    echo=False
)

df = pd.read_sql("SELECT * FROM people", con=engine)

print(df)

new_data = pd.DataFrame({'name': ['Jack', 'Bill', 'Bob'], 'age': [26, 90, 18]})
new_data.to_sql('people', con=engine, if_exists='append', index=False)
