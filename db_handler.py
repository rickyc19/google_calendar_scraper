import psycopg2

conn = psycopg2.connect(database="nature_notice",
                        host="localhost",
                        user="postgres",
                        password="Rc_1625497",
                        port="5432")

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE CalendarEvents(
        EventId int NOT NULL AUTO_INCREMENT
        EventName varchar(100),
        HostName varchar(100)
               )
    """
)