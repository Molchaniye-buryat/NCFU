import re

data_text = """
Посетите наши страницы:
Email: info@example.com (главный), support-team@corp.net (поддержка)
Дата: 25-05-2023, 01/01/2024, 12.02.2025.
Коды товаров: ID_PROD-1001, ITEM-20-A, ID-300-B.
Суммы: $150.50, 20 EUR, 500 RUB, £75.
"""
reg = r'[A-Za-z0-9._-]+@[A-Za-z0-9-]+[.][A-Za-z]{2,3}'
finder = re.findall(reg, data_text)
print(finder)

reg = r'[ID_PROD|ID]+-([0-9]+)'
finder = re.findall(reg, data_text)
print(finder)

reg = r'([0-9]{2}).([0-9]{2}).([0-9]{4})'
finder = re.findall(reg, data_text)
for day, month, year in finder:
	new_date = f'{year}-{month}-{day}'
print(new_date)

reg = r'[0-9]+ [EUR|RUB]+'
finder = re.findall(reg, data_text)
print(finder)