import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import os.path

dotenv_config =  "config.env"
if os.path.exists(dotenv_config):
    load_dotenv(dotenv_config)

data_base_login = os.getenv("data_base_login")
data_base_password = os.getenv("data_base_password")
data_base_name = os.getenv("data_base_name")

DSN = f"postgresql://{data_base_login}:{data_base_password}@localhost:5432/{data_base_name}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

client_input = input("Введите имя автора: ")
true_input = f"%{client_input}%"

Session = sessionmaker(bind=engine)
session = Session()

with open("test_data.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

for record in json_data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

for c in (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock)
        .join(Shop).join(Sale).filter(Publisher.name.like(true_input)).all()):
    print(c[0],"|", c[1],"|", c[2],"|", c[3])


session.close()
