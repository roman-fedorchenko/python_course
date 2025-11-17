#структура запису в файл:
# Name
# Question
# Answer
def Open(file_name, mode):

    try:

        file = open(file_name, mode)

    except:

        print("[info] File", file_name, "wasn't opened!")

        return None

    else:

        print("[info] File", file_name, "was opened!")

        return file

def Answer_the_question():
    file1=Open("students.txt", "r")
    print("Question:\n")
    lines = file1.readlines()
    print(lines[-1])
    answer=input("Enter your answer: ")
    file2=Open("students.txt", "a")
    file2.write(answer + "\n")
    file1.close()
    file2.close()
    print("[info] files closed!")
    

def Enter_new_question():
    file=Open("students.txt", "a")
    name=input("Enter your name: ")
    question=input("Enter your question: ")
    file.write(name + "\n")
    file.write(question + "\n")
    file.close()
    print("[info] file closed!")

def Show_all_file():
    file=Open("students.txt", "r")
    content=file.read()
    print("\nFile content:\n\n", content)
    file.close()
    print("[info] file closed!")

print("Practic work 8. File handling in Python")
print("Student: \nАфанасенко Віктор ППМР1-102\nБобро Мар'яна ППМР1-102\nФедорченко Роман ППМР1-104\n")
while True :
    x=int(input("\nMenu:\n1. Answer the question\n2. Enter new question\n3. Show all file\n4. Exit\n5. Run all(try for practic work)\nChoose an action (1-5): "))
    if x==1:
        Answer_the_question()
    elif x==2:
        Enter_new_question()
    elif x==3:
        Show_all_file()
    elif x==4:
        break
    elif x==5:
        Show_all_file()
        Answer_the_question()
        Enter_new_question()

#file1_name = "students.txt"