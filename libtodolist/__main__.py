from .tasks import Task, TaskList, PriorityLevel
from typing import List
import sys

def go_repl():

    def repl_help():
        print("""todolist CLI interface
    a: list all tasks
    u: list urgent priority tasks
    n: list normal priority tasks
    l: list low priority tasks
    c: create new task
    m: mark task as done
    d: delete task
    s: save task list
    ?: show this help
    q: quit
    """)


    fn = sys.argv[2] if len(sys.argv) > 2 else None

    list_manager = TaskList([])
    if fn:
        list_manager = TaskList.from_json(fn)

    def show_task(task: Task):
        index_in_list = list_manager.tasks.index(task) + 1
        print(f"#{index_in_list}\t{task}")

    def show_tasklist(tasks: List[Task]):
        for task in tasks:
            show_task(task)

    def handle_a():
        show_tasklist([a for a in list_manager.tasks if not a.is_deleted])

    def handle_u():
        l = [task for task in list_manager.tasks if task.priority == PriorityLevel.URGENT and not task.is_deleted]
        show_tasklist(l)

    def handle_n():
        l = [task for task in list_manager.tasks if task.priority == PriorityLevel.NORMAL and not task.is_deleted]
        show_tasklist(l)

    def handle_l():
        l = [task for task in list_manager.tasks if task.priority == PriorityLevel.LOW and not task.is_deleted]
        show_tasklist(l)

    def handle_c():
        priority = None
        title = input("\tPlease input task description: ")
        prios = {
            'l': PriorityLevel.LOW,
            'n': PriorityLevel.NORMAL,
            'u': PriorityLevel.URGENT
        }
        while priority is None:
            priority = input("\tPlease input priority (l/n/u) (default: n): ").lower()
            if not len(priority):
                priority = 'n'
            if priority[0] not in prios:
                priority = None
            priority = prios[priority[0]]
        list_manager.tasks.append(Task(priority=priority, name=title))
        print(f"\tCreated new task {title} with priority {priority}")

    def handle_d():
        l = input("\tInput the #number of the task you want to delete (empty input to cancel): ")
        if not len(l):
            print("\tCancelling")
            return
        task_num = int(l) - 1
        assert task_num >= 0
        assert task_num < len(list_manager.tasks)
        list_manager.tasks[task_num].is_deleted = True
        print(f"\tTask {task_num + 1} deleted")

    def handle_m():
        l = input("\tInput the #number of the task you want to mark as done (empty input to cancel): ")
        if not len(l):
            print("\tCancelling")
            return
        task_num = int(l) - 1
        assert task_num >= 0
        assert task_num < len(list_manager.tasks)
        list_manager.tasks[task_num].is_done = True
        print(f"\tTask {list_manager.tasks[task_num]} is done!")

    def handle_s():
        fn = input("Which file name to save to? (default: tasklist.json): ")
        if not len(fn):
            fn = "tasklist.json"
        list_manager.to_json(fn)
        print("Completed")

    def handle_q():
        print("bye!")
        sys.exit(0)

    fun_map = {
        'a': handle_a,
        'u': handle_u,
        'n': handle_n,
        'l': handle_l,
        'c': handle_c,
        'm': handle_m,
        'd': handle_d,
        's': handle_s,
        'q': handle_q,
        '?': repl_help,
    }

    repl_help()
    while True:
        a = input("a/u/n/l/c/d/s/q/?: ")
        f = fun_map.get(a, repl_help)
        f()

go_repl()
