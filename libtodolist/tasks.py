"""libtodolist.tasks: manage todo lists in python"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import List
import json

class PriorityLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    URGENT = "urgent"

def done_emoji(v: bool):
    if v:
        return "✅"
    else:
        return "⌛"

@dataclass
class Task:
    name: str
    priority: PriorityLevel = PriorityLevel.NORMAL
    is_done: bool = False
    is_deleted: bool = False

    def __str__(self):
        return f"""[{self.priority}] {self.name} | {done_emoji(self.is_done)}"""

@dataclass
class TaskList:
    tasks: List[Task]

    @classmethod
    def from_json(cls, json_file):
        data = None
        with open(json_file, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        assert data is not None
        tasks = []
        for list_item in data:
            l = Task(**list_item)
            tasks.append(l)
        return cls(tasks=tasks)
    
    def to_json(self, json_file):
        data = [asdict(t) for t in self.tasks if not t.is_deleted]
        with open(json_file, 'w', encoding='utf-8') as fh:
            json.dump(data, fh)