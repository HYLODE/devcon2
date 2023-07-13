# streamlit_app.py
import datetime
import time

import random
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import insert

def create_engine_ids():
    """Return SQLAlchemy Engine"""
    return create_engine(
        f"postgresql+psycopg2://postgres:postgres@db:5432/demo"
    )


engine = create_engine_ids()
metadata=MetaData()
ids_table = Table("tbl_ids_master", metadata, autoload_with=engine)

unid = 0

message_types = (
"MDM^T02", "ORM^O01", "ORR^O02", "ORU^R01", "ADT^A08", "ADT^A04", "ADT^A31", "ADT^A03", "ADT^A05",
"MDM^T08", "MDM^T11", "ADT^A01", "ORU^R30", "PPR^PC1", "ADT^A16", "ADT^A25", "ADT^A02", "ADT^A15",
"ADT^A28", "BTS^O31", "ADT^Z99", "PPR^PC2", "ADT^A60", "ADT^A06",
)
senderapplications = (
"EPIC", "IMG_END_EXAM", "IMG_RESULT", "Not In Message", "WinPath", "IMG_ARRIVE_APPT",
"ABL90 FLEX Plus", "IMG_CANCEL_APPT", "IMG_PRIOR_STATUS", "IMG_PROC_CHANGE",
"IMG_UNLINK", "IMG_MOPS_CHANGE", "IMG_LINK", "ELR_RESULT",
)

with engine.connect() as connection:
    while True:
        unid += 1
        data = {
            'unid': unid,
            "messagedatetime": datetime.datetime.now(),
            "messagetype": random.choice(message_types),
            "senderapplication": random.choice(senderapplications),
        }
        print(data)
        stmt = insert(ids_table).values(data)
        result = connection.execute(stmt)
        print("Insert OK") if result.rowcount == 1 else print("Insert failed")
        connection.commit()
        time.sleep(random.randint(0,999) / 1000)
