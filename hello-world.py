from sqlalchemy.orm import sessionmaker
from models import Tests, db_connect, create_test_table
from sqlalchemy.engine.url import URL

import numpy
import math
import csv
import random
import settings

engine = db_connect()
create_test_table(engine)
sessionmaker(bind=engine)
print("Hello, World")
print(engine)