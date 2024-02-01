from Task import Task, Status, encode_tasks, decode_tasks, decode_status
import json
from datetime import date, time, datetime
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def manager(tasks_file, history_file):
        print("------------------------------------------------------------------------------------")
        print("stop - остановить работу с менеджером задач")
        print("list - просмотреть список задач")
        print("add - добавить задачу")
        print("history n - просмотреть последние n изменений (введите 0 если хотите посмотреть все)")
        print("delete n - удалить задачу под номером n")
        print("open n - просмотр задачи с номером n")
        print("promote - продвинуть статус выполнения задачи")
        print("demote - отодвинуть статус выполнения задачи")
        print("cancel - отменить выполнение задачи")
        print("close - окончить просмотр задачи (изменения сохранятся автоматически)")

        with open(tasks_file, "r") as f:
            tasks = decode_tasks(json.load(f))


        while True:
            order = input().split()
            if order == []:
                pass
            #остановка работы менеджера
            elif order[0] == "stop":
                break
            #вывод списка задач
            elif order[0] == "list":
                print("------------------------------------------------------------------------------------")
                for i in range(len(tasks)):
                    print(str(i + 1) + ': ', tasks[i].name)
                print("------------------------------------------------------------------------------------")
            #добавление задачи
            elif order[0] == "add":
                print("------------------------------------------------------------------------------------")
                new_name = input("Введите название: ")
                new_description = input("Введите описание: ")
                new_date_of_creation = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                tasks.append(Task(new_name, new_description, Status.NEW, new_date_of_creation, new_date_of_creation))
                print("------------------------------------------------------------------------------------")
            #открытие задачи    
            elif order[0] == "open" and order[-1].isdigit():
                if int(order[1]) > len(tasks) or int(order[1]) == 0:
                    print("Задачи с таким номером не существует")
                else:
                    print("------------------------------------------------------------------------------------")
                    with open(history_file, "a") as f:
                        f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - Открыта задача ' + order[1] + '\n')
                    opened_task = tasks[int(order[1]) - 1]
                    print("Задача: ", opened_task.name)
                    print("Описание: ", opened_task.description)
                    print("Статус: ", opened_task.status.name)
                    print("Дата создания: ", opened_task.date_of_creation)
                    print("Дата изменения: ", opened_task.date_of_status_change)
                    while True:
                        task_order = input()
                        if task_order == "promote":
                            if opened_task.status.name == "COMPLETED":
                                print("Повысить статус выполнения задачи нельзя, задача уже завершена")
                            else:
                                opened_task.promote()
                                print("Статус задачи: ", opened_task.status.name)
                        elif task_order == "demote":
                            if opened_task.status.name == "NEW":
                                print("Понизить статус выполнения задачи нельзя, к выполнению задачи ещё не приступали")
                            elif opened_task.status.name == "CANCELLED":
                                print("Понизить статус выполнения задачи нельзя, задача находится в статусе 'отменено'")
                            else:
                                opened_task.demote()
                                print("Статус задачи: ", opened_task.status.name)
                        elif task_order == "cancel":
                            if opened_task.status.name == "CANCELLED":
                                print("Задача уже отменена")
                            else:
                                opened_task.cancel()
                                print("Задача отменена")
                        elif task_order == "close":
                            tasks[int(order[1]) - 1] = opened_task
                            break
                        else:
                            print("Команда не распознана")
                    print("------------------------------------------------------------------------------------")
            #удаление задачи
            elif order[0] == "delete" and order[-1].isdigit():
                if int(order[1]) > len(tasks) or int(order[1]) == 0:
                    print("Задачи с таким номером не существует")
                else:
                    del tasks[int(order[-1]) - 1]
                    print("Задача " + order[-1] + " удалена")

            #вывод истории
            elif order[0] == "history" and order[-1].isdigit():
                print("------------------------------------------------------------------------------------")
                n = int(order[1])
                with open(history_file, "r") as f:
                    history = f.read().split("\n")
                if n > len(history) or n == 0: n = len(history)
                for i in range(1, n + 1):
                    print(history[len(history) - i - 1])
                print("------------------------------------------------------------------------------------")
            else:
                print("Команда не распознана")

            
            #сохранение задач
            with open(tasks_file, "w") as f:
                json.dump(encode_tasks(tasks), f, indent=4)                        