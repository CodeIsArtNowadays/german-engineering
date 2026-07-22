from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session, declarative_base, Mapped, mapped_column


engine = create_engine(
    "sqlite:///multi_agent/maDATA.db", connect_args={"autocommit": False}
)

local_session = sessionmaker(bind=engine)

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column()
    time: Mapped[datetime] = mapped_column()

class NoteModel(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str] = mapped_column()



def create_task(description: str, time: str):
    if not time: # Если пришла пустая строка
        return {"status": "error", "message": "Time field cannot be empty. Please calculate the exact date and time first."}
        
    try:
        datetime_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            datetime_obj = datetime.strptime(time, "%Y-%m-%d")
        except ValueError:
            # Возвращаем ошибку АГЕНТУ, а не роняем скрипт!
            return {"status": "error", "message": f"Invalid time format {time}"} 
    with local_session.begin() as session:
    
        task = TaskModel(task=description, time=datetime_obj)
        session.add(task)
        session.flush()
        session.refresh(task)
        return {"status": "success", "message": "Task successfully saved to database"}

def create_note(description: str):
    with local_session.begin() as session:

        note = NoteModel(note=description)
        session.add(note)
        session.flush()
        session.refresh(note)
        return {"status": "success", "message": "Note successfully saved to database"}