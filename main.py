import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import os.path
from dotenv import load_dotenv


dotenv_config =  "config.env"
if os.path.exists(dotenv_config):
    load_dotenv(dotenv_config)

data_base_login = os.getenv("data_base_login")
data_base_password = os.getenv("data_base_password")
data_base_name = os.getenv("data_base_name")

DSN = f"postgresql://{data_base_login}:{data_base_password}@localhost:5432/{data_base_name}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)


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

def get_shops(client_input):
    find_publisher = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale
    ).select_from(Shop).\
        join(Stock).\
        join(Book).\
        join(Publisher).\
        join(Sale)
    if client_input.isdigit():
        result_search = find_publisher.filter(client_input == Publisher.id).all()
    else:
        result_search = find_publisher.filter(client_input == Publisher.name).all()
    for title, name, price, date_sale in result_search:
        print(f"{title} | {name} | {price} | {date_sale.strftime('%d-%m-%Y')}")
    session.close()


if __name__ == '__main__':
    client_input = input("Введите имя или id автора: ")
    get_shops(client_input)
