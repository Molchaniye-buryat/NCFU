menu = {
    "паста": 300,
    "пицца": 700,
    "доширак": 70,
    "суп": 200,
    "шаурма": 550
}

orders = []

def adding():
    name = input('Введите название блюда: ')
    price = int(input('Введите цену блюда: '))
    menu[name] = price
    print(f'блюдо {name} добавлено')


def order_creating():
    table = int(input('Введите номер столика: '))
    print(f'Наше меню: {menu}')
    dish_order = {}
    while True:
        dish = input('Введите блюдо для заказа и напишите СТОП для завершения: ')
        if dish == 'СТОП' or dish == 'стоп':
            break
        if dish in menu:
            cnt = int(input('Кол-во: '))
            dish_order[dish] = cnt
        else:
            print('Такого блюда нет')
    total = 0
    for dish, cnt in dish_order.items():
        total = total + menu[dish]*cnt
    order = {
        'Номер столика:': table,
        'блюда': dish_order,
        'стоимость': total
    }
    orders.append(order)
    print(f'Заказ создан, общая стоимость: {total}')
    print(order)
def total_money():
    total = 0
    for order in orders:
        total = total + order['стоимость']
    print(f'Общая вырука составляет: {total}')

while True:
    print('')
    print('Возможные команды:')
    print('1.Добавить блюдо')
    print('2.Создать заказ')
    print('3.Общая выручка')
    print('4.Выход')
    print('')

    choice = input('Выберите действие: ')
    if choice == '1':
        adding()
    elif choice == '2':
        order_creating()
    elif choice == '3':
        total_money()
    else:
        print('Непрвильная команда')
 

