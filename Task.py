from dataclasses import dataclass
from enum import Enum
from datetime import date, datetime
import json

class Status(Enum):
    CANCELLED = 0
    NEW = 1
    IN_PROGRESS = 2
    REVIEW = 3
    COMPLETED = 4

    
def decode_status(status):
    if status == "CANCELLED":
        return Status.CANCELLED
    elif status == "NEW":
        return Status.NEW
    elif status == "IN_PROGRESS":
        return Status.IN_PROGRESS
    elif status == "REVIEW":
        return Status.REVIEW
    elif status == "COMPLETED":
        return Status.COMPLETED

#класс задачи
@dataclass
class Task:
    name: str
    description: str
    status: Status
    date_of_creation: str
    date_of_status_change: date

    def promote(self):
        if self.status.name == "CANCELLED":
            self.status = Status.NEW        
        elif self.status.name == "NEW":
            self.status = Status.IN_PROGRESS
        elif self.status.name == "IN_PROGRESS":
            self.status = Status.REVIEW
        elif self.status.name == "REVIEW":
            self.status = Status.COMPLETED
        self.date_of_status_change = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def demote(self):
        if self.status.name == "COMPLETED":
            self.status = Status.REVIEW
        elif self.status.name == "REVIEW":
            self.status = Status.IN_PROGRESS
        elif self.status.name == "IN_PROGRESS":
            self.status = Status.NEW
        self.date_of_status_change = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def cancel(self):
        self.status = Status.CANCELLED
        self.date_of_status_change = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#перевод списка из Task в список из словарей
def encode_tasks(list_of_tasks):
    new_list = []
    for task in list_of_tasks:
        new_list.append(
            {"name": task.name, 
            "description": task.description, 
            "status": task.status.name, 
            "date_of_creation": task.date_of_creation,
            "date_of_status_change": task.date_of_creation
            }
            )
    return new_list
        
#перевод из словарей в список из Task        
def decode_tasks(list_of_tasks):
    new_list = []
    for task in list_of_tasks:
        new_list.append(Task(task["name"], task["description"], decode_status(task["status"]), task["date_of_creation"], task["date_of_status_change"]))
    return new_list


