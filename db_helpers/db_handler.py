import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Union, Any
from db_schemas import EventHost, CalendarEvent
from sqlalchemy.dialects.postgresql import insert



class DBHandler:
    def __init__(self):
        url = URL.create(
            drivername="postgresql",
            username="postgres",
            host="localhost",
            database="postgres",
            password="Rc_1625497"
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

        inserted_id = self.session.execute(
            on_conflict_statement
        ).scalar()

        self.session.commit()

        return inserted_id

    def upsert_calendar_events_table(
            self,
            calendar_event_dict: Dict[str, str]
    ) -> int:
        return self.upsert_into_table(
            CalendarEvent,
            calendar_event_dict,
            [CalendarEvent.host_id, CalendarEvent.host_event_id]
        )

    def upsert_event_hosts_table(
            self,
            event_host_dict: Dict[str, str]
    ) -> int:
        return self.upsert_into_table(
            EventHost,
            event_host_dict,
            [EventHost.host_calendar_id]
        )


event_hosts_dict = {"host_calendar_id": "1", "host_name": "Test"}
db_handler = DBHandler()
row_id = db_handler.upsert_event_hosts_table(event_hosts_dict)
print(row_id)
