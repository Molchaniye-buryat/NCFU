def INN_check():
    while True:
        INN_input = input("Введите ваш ИНН: ")
        try:
            INN = int(INN_input)
            if 100000000000 <= INN < 1000000000000:
                print(f"ИНН принят: {INN}")
                return INN
            else:
                print("ИНН должен состоять из 12 цифр")
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите целое число")
INN_check()

def coast_check():
    while True:
        coast_input = input("Введите цену: ")
        try:
            coast = float(coast_input)
            if 0 <= coast <= 1000000:
                print(f"Цена принята: {coast}")
                return coast
            else:
                print("Цена не должна превышать 1_000_000")
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите целое число")
coast_check()

import re
reg = r'[A-Za-z0-9]+'
def password_check():
    while True:
        password = input("Введите ваш пароль: ").strip()
        if re.fullmatch(reg, password) and any(c.isupper() for c in password) and any(b.isdigit() for b in password) and 8<=len(str(password))<=20:
            print(f"Пароль принят: {password}")
            return password
        else:
            print("Неверный формат пароля. Он должен содержать минимум одну заглавную букву и цифру. Длина пароля должна быть от 8 до 20 символов")
password_check()