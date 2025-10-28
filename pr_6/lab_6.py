# Створення та управління словником студентів

students = {
    "student1": {
        "first_name": "Viktor",
        "last_name": "Afanasenko",
        "course": 2,
        "grades": {"Python": 4, "Numerical Methods": 4, "elective course": 5}
    },
    "student2": {
        "first_name": "Roman",
        "last_name": "Fedorchenko",
        "course": 2,
        "grades": {"Python": 5, "Numerical Methods": 5, "elective course": 3}
    },
    "student3": {
        "first_name": "Mariyana",
        "last_name": "Bobro",
        "course": 2,
        "grades": {"Python": 4, "Numerical Methods": 5, "elective course": 5}
    }
}
# Виведення початкового словника студентів
def show() : 
    for key, value in students.items():
        print(f"{key}: {value}")
    print("\n")
# Функція Афанасенка В.Ю.
# Функція додавання нових студентів
def add ():
    n = int(input("Скільки студентів ви хочете додати? "))
    for i in range(1, n + 1):
        key = f"student{i + 3}"  # виправлено проблему з пробілом у ключі
        students[key] = {}

        name = input(f"\nВведіть ім'я для {key}: ")
        students[key]["first_name"] = name
        last_name = input(f"\nВведіть прізвище для {key}: ")
        students[key]["last_name"] = last_name
        course = input("\nВведіть курс студента: ")
        students[key]["course"] = course
        students[key]["grades"] = {}

        m = int(input(f"Скільки предметів у {name}? "))
        for _ in range(m):
            subject = input("Введіть назву предмета: ")
            grade = int(input("Введіть оцінку: "))
            students[key]["grades"][subject] = grade
    #use new function show()
        print("\nОновлений cловник студентів та їх оцінок:")
    show()
# Функція Федорченка Р.С.
#insert sort_by_name function here
def sort_by_name(students_dict):
    #create a list of tuples (key, value) and sort it by first_name
    sorted_items = sorted(students_dict.items(), key=lambda x: x[1]["first_name"])
    # Return a new dictionary sorted by first names
    print("\nВідсортований за ім'ям студента словник студентів та їх оцінок:")
    show()
    return dict(sorted_items)

 # Функція Бобро М.Г.
 # Функція для видалення студента зі словника
def remove_student(students_dict):
    print("\nСписок студентів:")
    for key in students_dict.keys():
        print(f" - {key}") # Виводимо всі ключі студентів
    student_key = input("\nВведіть ключ студента, якого потрібно видалити (наприклад, student2): ")

    if student_key in students_dict: # Перевірка чи існує такий студент
        del students_dict[student_key] # Видаляємо студента зі словника
        print(f"Студента '{student_key}' успішно видалено.")
    else:
        print(f"Студента з ключем '{student_key}' не знайдено.")

    #Виводимо оновлений словник студентів
    print("\nОновлений список студентів:")
    show()
while True :
    x=int(input("1.  Вивести словник  \n2.  Додати елемент у словник  \n3.  Видалити елемент зі словника  \n4.  Відсортувати словник  \n5.  Закрити програму  \n Виберіть дію (1-5):"))
    if x == 1 :
        print("\nСловник студентів та їх оцінок:")
        show()
    elif x==2:
        add()
    elif x==3:
         remove_student(students)
    elif x==4:
        students = sort_by_name(students)
    elif x==5:
        break