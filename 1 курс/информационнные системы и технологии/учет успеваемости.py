students = {}
grades = []
def student_add():
	student_id = input('ID студента: ')
	student_name = input('ФИО студента: ')
	student_group = input('Группа студента: ')
	student_contacts = input('Номер телефона студента: ')

	students[student_id] = {
		'ФИО': student_name,
		'Группа': student_group
	}
	print(f'Студент {student_name} добавлен')
	

def grade_add():
        student_id = input('ID студента: ')
        if student_id not in students:
                print('Студент не найден')
                pass
        subject = input('Предмет: ')
        grade = int(input('Оценка: '))
        date = input('Дата: ')

        grades.append({
                'id': student_id,
                'Предмет': subject,
                'Оценка': grade,
                'Дата': date
        })
        print('Оценка добавлена')

def student_average():
        student_id = input('ID студента: ')
        student_grades = []
        for grade in grades:
                if grade['id'] == student_id:
                        student_grades.append(grade['Оценка'])
        if student_grades:
            avg = sum(student_grades)/len(student_grades)
            name = students[student_id]
            print(f'Средний балл {name}: {avg:}')
        else:
            print('Оценок нет')
def bad_students():
    bad_grade = int(input('Ниже какой оценки искать? '))

    bad_students = {}
    for grade in grades:
        if grade['Оценка'] < bad_grade:
            student_id = grade['id']
            student_name = students[student_id]
            print(f"{student_name}: {grade['Оценка']} по {grade['Предмет']}")

while True:
    print('')
    print("Учет успеваемости")
    print("1. Добавить студента")
    print("2. Добавить оценку")
    print("3. Средний балл студента")
    print("4. Студенты с плохими оценками")
    print("5. Выход")
    print('')

    choice = input('Выберите действие: ')
    if choice == '1':
        student_add()
    elif choice == '2':
        grade_add()
    elif choice == '3':
        student_average()
    elif choice == '4':
        bad_students()
    elif choice == '5':
        break
    else:
        print('Неверный выбор')
    
    
                  
                        

        





