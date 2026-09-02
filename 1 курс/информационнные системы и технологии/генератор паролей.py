import random
while True:
  letters = 'abcdefghijklmnopqrstuvoxyz'
  digit = '0123456789'
  symbol = '!@#$%^8*-№?'
  cnt = int(input('Сколько паролей сгенерировать?'))
  len = int(input("Длина пароля:"))
  letters_check = input("Нужны ли буквы в пароле? (y/n)")
  digit_check = input("Нужны ли цифры в пароле? (y/n)")
  symbol_check = input("Нужны ли спец. символы в парое? (y/n)")
  if letters_check == 'n':
      letters = ''
  if digit_check == 'n':
      digit = ''
  if symbol_check == 'n':
      symbol = ''
  all_symbols = letters+digit+symbol
  for a in range(cnt):
    password = ''
    for i in range(len):
        random_symbol = random.choice(all_symbols)
        password = random_symbol + password
    print(password)