import psycopg2
import logging
from sqlalchemy import create_engine

class Connection:
    def get_connection(self, user, password):
        try:
            connection = psycopg2.connect(database="abhishek", user=user, password=password, host="localhost", port=5433)
            return connection
        except:
            logging.error("Connection Error!")
            raise Exception("Connection Error!")
        finally:
            logging.info("Database connected")

    def get_engine(self, user, password):
        if user != "abhishek":
            raise Exception("Wrong user")

        try:
            engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5433/abhishek")
            return engine
        except:
            logging.error("Engine creation error!")
        finally:
            logging.info("Engine created")
