from utils.stock import fetch_filtered_stock_list

from db.database import get_session
from app.models.stock import Stock


class StockRepository:

    @staticmethod
    def process_batch(batch, session):
        """
        Обрабатывает батч: добавляет новые записи или обновляет существующие.
        """
        existing_symbols = {
            stock.symbol for stock in session.query(Stock).filter(
                Stock.symbol.in_([item["symbol"] for item in batch if "symbol" in item])
            ).all()}

        for stock in batch:
            if stock.get("name") and stock.get("symbol") and stock.get("price"):
                if stock["symbol"] in existing_symbols:
                    # Обновляем существующую запись
                    existing_stock = session.query(Stock).filter_by(symbol=stock["symbol"]).one()
                    existing_stock.name = stock["name"]
                    existing_stock.price = stock["price"]
                else:
                    # Добавляем новую запись
                    new_stock = Stock(
                        symbol=stock["symbol"],
                        name=stock["name"],
                        price=stock["price"],
                    )
                    session.add(new_stock)

    @staticmethod
    def insert_stock_to_db( batch_size=1000):
        """
        Обновляет или добавляет акции в базе данных по батчам.
        """

        stock_list = fetch_filtered_stock_list()

        for i in range(0, len(stock_list), batch_size):
            batch = stock_list[i:i + batch_size]
            with get_session() as session:
                StockRepository.process_batch(batch, session)
                session.commit()  # Фиксируем изменения после обработки батча
        print("Stock list processed and updated in database.")
