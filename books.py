# Importation de la bibliothèque
import requests
from bs4 import BeautifulSoup
import os
import csv


# Le fonction get_product_info qui renvoit le lien de chaque livre et retourne les données le concernant

def get_product_info(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    resultats = soup.findAll("div", attrs={"class": "container-fluid page"})
    for resultat in resultats:
        product_page_url = url
        universal_product_code = soup.find("td").text
        title = soup.find("h1").text
        price_including_tax = soup.findAll("td")[3].text
        price_excluding_tax = soup.findAll("td")[2].text
        number_available = soup.findAll("td")[5].text
        product_description = soup.findAll("p")[3].text
        category = soup.findAll("li")[2].text
        review_rating = soup.find("p", "star-rating")["class"][-1]
        image_url = soup.find("img")["src"]
        book_ref = {
            "product_page_url": product_page_url,
            "universal_product_code": universal_product_code,
            "title": title,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "number_available": number_available,
            "product_description": product_description,
            "category": category,
            "review_rating": review_rating,
            "image_url": image_url,
        }
        return book_ref

# La fonction get_categories_info recupère le lien de chaque categorie et retourne le lien de chaque article de livre
def get_categorie_info(link_cat,category_name):

    reponse = requests.get(link_cat)
    soup = BeautifulSoup(reponse.text, "html.parser")
    book_links = soup.findAll("h3")
    for h3 in book_links:
        a = h3.find("a")
        link = a["href"][9:]
        url_book = "http://books.toscrape.com/catalogue/" + link

        #We save the current book in the current category by appending it to the csv file
        book_infos = get_product_info(url_book)
        save_product_info(category_name,book_infos)




def save_product_info(category_name,data):


    #Check if category file exists
    if os.path.isfile('categories/' + category_name +'.csv'):
        with open('categories/' + category_name +".csv","a",newline="", encoding="utf-8") as category_file:
            csv_writer = csv.writer(category_file)
            csv_writer.writerow([data['product_page_url'], data['universal_product_code'], data['title'], data['price_including_tax'], data['price_excluding_tax'], data['number_available'], data['product_description'], data['category'], data['review_rating'], data['image_url']])
    else:
        with open('categories/' + category_name +".csv","a",newline="", encoding="utf-8") as category_file:
            csv_writer = csv.writer(category_file)
            csv_writer.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
            csv_writer.writerow([data['product_page_url'], data['universal_product_code'], data['title'], data['price_including_tax'], data['price_excluding_tax'], data['number_available'], data['product_description'], data['category'], data['review_rating'], data['image_url']])



"""# Fonction  qui pretourne l'url de la pagination d'une catégorie quand celle_ci en dispose

def get_cat_pagination_info(link_cat):
    reponse = requests.get(link_cat)
    soup = BeautifulSoup(reponse.text,"html.parser")
    pager = soup.findAll("li", attrs={"class": "next"})
    for li in pager:
        a = li.find("a")
        link_page = a["href"]
        suivant = "http://books.toscrape.com/catalogue/category/books/romance_8/" + link_page
"""


# Fonction all_categories qui recupère et retourne le lien de chaque catégirie
def get_all_categorie(url):

    #Create directory where we will save all the files
    try:
        os.mkdir('./categories')
    except Exception as e:
        pass


    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    cat_links = soup.findAll("ul", attrs={"class": "nav nav-list"})
    for ul in cat_links:
        cat_link = ul.findAll("a")[1:]
        for link in cat_link:
            if "href" in link.attrs:
                link_cat = "http://books.toscrape.com/" + link.attrs["href"]

                #get category name. Strip method is useful to remove white spaces around the category name
                category_name = link.string.strip()

                get_categorie_info(link_cat,category_name)

get_all_categorie("http://books.toscrape.com/index.html")
