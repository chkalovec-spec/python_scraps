from bs4 import BeautifulSoup
import requests
import os
import csv

encoding = "utf_8_sig"
domain = 'https://health-diet.ru'
main_url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
final_folder_path = "./data/heealt_diet_data/"

req_headers = {
  'Accept': '*/*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
req = requests.get(main_url, headers=req_headers)
src = req.text

soup = BeautifulSoup(src, 'lxml')
all_products_links = soup.find_all('a', class_="mzr-tc-group-item-href")

all_categories_dict = {}

for product in all_products_links:
  product_text = product.text
  product_link = domain + product.get("href")
  all_categories_dict[product_text] = product_link

iteration_count = int(len(all_categories_dict))

for category_name, category_link in all_categories_dict.items():
  print(f"{category_name}: Запись начата")
  req = requests.get(url=category_link, headers=req_headers)
  src = req.text

  soup = BeautifulSoup(src, 'lxml')
  
  if (soup.find(class_="uk-alert-danger") is not None):
    iteration_count -=1
    print(f"{category_name}: Данные отсутствуют (осталось: {iteration_count})")
    continue
  
  products_heads = soup.find("table", class_="mzr-tc-group-table").find("thead").find_all("th")
  
  product = products_heads[0].text
  calories = products_heads[1].text
  proteins = products_heads[2].text
  fats = products_heads[3].text
  carbohydrates = products_heads[4].text

  if not os.path.exists(final_folder_path): os.makedirs(final_folder_path) 

  with open(f"{final_folder_path}{category_name}.csv", "w", encoding=encoding) as file:
    writter = csv.writer(file)
    writter.writerow((product, calories, proteins, fats, carbohydrates))

  products_data = soup.find("table", class_="mzr-tc-group-table").find("tbody").find_all("tr")
  
  for product in products_data:
    product_tds = product.find_all("td")
    
    title = product_tds[0].find("a").text
    calories = product_tds[1].text
    proteins = product_tds[2].text
    fats = product_tds[3].text
    carbohydrates = product_tds[4].text
    
    with open(f"{final_folder_path}{category_name}.csv", "a", encoding=encoding) as file:
      writter = csv.writer(file)
      writter.writerow((title, calories, proteins, fats, carbohydrates))
  
  iteration_count -=1
  print(f"{category_name}: Запись завершена (осталось: {iteration_count})")

  if iteration_count == 0:
    final_folder = os.path.abspath(f'{final_folder_path}')
    print(f"Данные сохранены в папку {final_folder}")