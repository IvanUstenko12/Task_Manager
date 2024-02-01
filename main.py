from Manager import manager

tasks_file = input("Введите название json файла с задачами: ")
history_file = input("Введите название txt файла с историей: ")
manager(tasks_file, history_file)