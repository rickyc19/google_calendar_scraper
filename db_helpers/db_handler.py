import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Union, Any
from db_schemas import EventHost, CalendarEvent
from sqlalchemy.dialects.postgresql import insert

print(os.environ.get("DB_PASSWORD"))


class DBHandler:
    def __init__(self):
        url = URL.create(
            drivername="postgresql",
            username="naturenotice",
            host=os.environ.get("DB_HOST"),
            database="db_nature_notice",
            password=os.environ.get("DB_PASSWORD")
        )

        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def upsert_into_table(self, table, data_dict, index_elements) -> int:
        insert_statement = insert(table).values(data_dict)

        on_conflict_statement = insert_statement.on_conflict_do_update(
            set_=data_dict,
            index_elements=index_elements
        ).returning(table.id)

        inserted_id = self.session.execute(on_conflict_statement).scalar()

        self.session.commit()

        return inserted_id

    def upsert_calendar_events_table(self, calendar_event_dict: Dict[str, str]) -> int:
        return self.upsert_into_table(
            CalendarEvent,
            calendar_event_dict,
            [CalendarEvent.host_id, CalendarEvent.host_event_id]
        )

    def upsert_event_hosts_table(self, event_host_dict: Dict[str, str]) -> int:
        return self.upsert_into_table(
            EventHost,
            event_host_dict,
            [EventHost.host_calendar_id]
        )


now = datetime.datetime.utcnow().isoformat()
cal_event_dict = {"host_id": "1",
                  "host_event_id": "2",
                  "event_name": "Test",
                  "event_description": "Test",
                  "event_price": 0,
                  "event_start_date": now,
                  "event_end_date": now,
                  "event_location": "Test"}
db_handler = DBHandler()
row_id = db_handler.upsert_calendar_events_table(cal_event_dict)
print(row_id)
