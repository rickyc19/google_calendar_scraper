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

    def insert_calendar_events_table(self, calendar_event_dict_list: List[Dict[str, Union[str, int]]]) -> None:
        insert_statement = insert(CalendarEvent).values(calendar_event_dict_list)
        do_nothing_statement = insert_statement.on_conflict_do_nothing(index_elements=["host_id", "host_calendar_id"])
        self.session.execute(do_nothing_statement)
        self.session.commit()

    def insert_event_hosts_table(self, event_host_dict: Dict[str, str]) -> Any:
        insert_statement = insert(EventHost).values(host_calendar_id=event_host_dict["id"], host_name=event_host_dict["summary"])
        do_nothing_statement = insert_statement.on_conflict_do_nothing(index_elements=[EventHost.host_calendar_id]).returning(EventHost.host_id)
        inserted_id = self.session.execute(do_nothing_statement).fetchone()[0]
        self.session.commit()
        return inserted_id

event_hosts_dict = {"id": "1", "summary": "Test"}
db_handler = DBHandler()
row_id = db_handler.insert_event_hosts_table(event_hosts_dict)
print(row_id)
