menu = {
    "pizza": 700,
    "pasta": 300,
    "doshirak": 70,
    "soup": 200,
    "shawerma": 550
}

orders = []

def adding():
    name = input('Введите название блюда: ')
    price = input('Введите цену блюда: ')
    menu[name] = price
    print(f'блюдо {name} добавлено')


def order_creating():
    table = input('Введите номер столика: ')
    print(f'Наше меню: {menu}')
    dish_order = {}
    while True:
        dish = input('Введите блюдо для заказа и напишите СТОП для завершения: ')
        if dish == 'STOP' or dish == 'stop':
            break
        if dish in menu:
            cnt = int(input('Кол-во: '))
            dish_order[dish] = cnt
        else:
            print('ди наху')
order_creating()
