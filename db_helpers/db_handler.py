from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Union
from db_schemas import EventHosts, CalendarEvent
from sqlalchemy.dialects.postgresql import insert

event_hosts_dict = {"id": "1", "summary": "Test"}

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
        self.session.add(do_nothing_statement)
        self.session.commit()

    def insert_event_hosts_table(self, event_hosts_dict: Dict[str, str]) -> int:
        insert_statement = insert(EventHosts).values(host_calendar_id=event_hosts_dict["id"], host_name=event_hosts_dict["summary"])
        do_nothing_statement = insert_statement.on_conflict_do_nothing(index_elements=["host_calendar_id"])
        self.session.add(do_nothing_statement)
        self.session.commit()
        return self.session.inserted_primary_key

