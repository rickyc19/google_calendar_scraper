from db_handler import DBHandler
from calendar_handler import CalendarScraperHandler
from ai_handler import ai_summarizer


def main():
    calendar_scraper = CalendarScraperHandler()
    calendar_list = calendar_scraper.get_calendar_list()
    calendar_events_dict = {}
    for calendar in calendar_list:
        calendar_id = calendar["host_calendar_id"]
        calendar_events = calendar_scraper.get_calendar_events(calendar_id)
        calendar_events_dict[calendar_id] = calendar_events

    print(calendar_events_dict)

    db_handler = DBHandler()

    for calendar in calendar_list:
        host_id = db_handler.upsert_event_hosts_table(calendar)
        print(host_id)
        for event_dict in calendar_events_dict[calendar["host_calendar_id"]]:
            print(f"Event: {event_dict}")
            event_dict["host_id"] = host_id
            event_dict["event_description"] = ai_summarizer(event_dict["event_description"])
            db_handler.upsert_calendar_events_table(event_dict)


if __name__ == '__main__':
    main()
