from os import path

file_base = "base.txt"
all_data = []
last_id = 0

if not path.exists(file_base):
    with open(file_base,"w",encoding="utf-8") as _:
        pass

def read_records():
    """Считывание данных"""
    global all_data, last_id

    with open(file_base, encoding="utf-8") as f:
        all_data = [i.strip() for i in f]
        if all_data:
            last_id = int(all_data[-1][0])
        return all_data


def show_all():
    """Отображение содержимого базы данных"""

    if not all_data:
        print("Введите номер")
    else:
        print(*all_data,sep="\n")


def add_new_contact():
    """Добавление новой записи"""

    global last_id

    array = ['surname', 'name', 'patronymic', 'phone number']
    answers = []
    for i in array:
        answers.append(data_collection(i))

    if not exist_contact(0, " ".join(answers)):
        last_id += 1
        answers.insert(0, str(last_id))

        with open(file_base, 'a', encoding="utf-8") as f:
            f.write(f'{" ".join(answers)}\n')
        print("Контакт успешно сохранен в телефонный справочник")
    else:
        print("Такой контакт уже есть..")



def del_contact():
    """Удаление записи"""

    global all_data

    symbol = "\n"
    show_all()
    del_record = input("Введите id записи для удаления: ")

    if exist_contact(del_record, ""):
        all_data = [k for k in all_data if k[0] != del_record]

        with open(file_base, 'w', encoding="utf-8") as f:
            f.write(f'{symbol.join(all_data)}\n')
            print("Запись удалена!\n")
    else:
        print("id не найден")



def change_contact(data_tuple):
    """Изменение существующей записи"""

    global all_data
    symbol = "\n"

    record_id, num_data, data = data_tuple

    for i, v in enumerate(all_data):
        if v[0] == record_id:
            v = v.split()
            v[int(num_data)] = data
            if exist_contact(0, " ".join(v[1:])):
                print("Запись изменена")
                return
            all_data[i] = " ".join(v)
            break
    with open(file_base, 'w', encoding="utf-8") as f:
            f.write(f'{symbol.join(all_data)}\n')
            print("Запись изменена!\n")


def exist_contact(rec_id, data):
    """Проверка записи в базе данных"""

#data проверка записи \ rec_id проверка id

    if rec_id:
        candidates = [i for i in all_data if rec_id in i[0]]
    else:
        candidates = [i for i in all_data if data in i]
    return candidates


def data_collection(num):
    """Проверка полученных данных"""

    answer = input(f"Введите {num}: ")
    while True:
        if num in "surname name patronymic":
            if answer.isalpha():
                break
        if num == "phone number":
            if answer.isdigit() and len(answer) == 11:
                break
        answer = input(f"Ошибка, попробуйте снова\n")

    return answer

def main_menu():
    """Основное меню"""

    play = True
    while play:
        read_records()
        answer = input("Телефонный справочник:\n"
                        "1. Показать все записи\n"
                        "2. Добавить запись\n"
                        "3. Изменить\n"
                        "4. Удалить\n"
                        "5. Экспорт\n"
                        "6. Выход\n")
        match answer:
            case "1":
                show_all()
            case "2":
                add_new_contact()
            case "3":
                work = edit_menu()
                if work:
                    change_contact(work)
            case "4":
                del_contact()
            case "5":
                exp_menu()
            case "6":
                play = False
            case _:
                print("Что-то пошло не так, повторите попытку!\n")

def edit_menu():
    """Меню редактирования"""

    add_dict = {"1": "surname", "2": "name", "3": "patronymic", "4": "phone number"}

    show_all()
    record_id = input("Введите id записи, которую хотите изменить: ")

    if exist_contact(record_id, ""):
        while True:
            print("\nChanging:")
            change = input("1. surname\n"
                           "2. name\n"
                           "3. patronymic\n"
                           "4. phone number\n"
                           "5. exit\n")

            match change:
                case "1" | "2" | "3" | "4":
                    return record_id, change, data_collection(add_dict[change])
                case "5":
                    return 0
                case _:
                    print("Данные не корректны")
    else:
        print("Данные не корректны")


def exp_bd(name):
    """Сохранение данных в новый файл"""

    symbol = "\n"

    if not path.exists(name):
        with open(f"{name}.txt", "w", encoding="utf-8") as f:
            f.write(f'{symbol.join(all_data)}\n')

def exp_menu():
    """Меню экспорта'"""

    while True:
        print("\nExp menu:")
        move = input("1. Export\n"
                     "2. exit\n")

        match move:
            case "1":
                exp_bd(input("Enter the name of the file: "))
            case "2":
                return 0
            case _:
                print("Данные не корректны")


main_menu()