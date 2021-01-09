# Importation de la bibliothèque
import requests
from bs4 import BeautifulSoup



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
def get_categorie_info(link_cat):
    reponse = requests.get(link_cat)
    soup = BeautifulSoup(reponse.text, "html.parser")
    book_links = soup.findAll("h3")
    for h3 in book_links:
        a = h3.find("a")
        link = a["href"][9:]
        url_book = "http://books.toscrape.com/catalogue/" + link
        print(get_product_info(url_book))


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
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    cat_links = soup.findAll("ul", attrs={"class": "nav nav-list"})
    for ul in cat_links:
        cat_link = ul.findAll("a")[1:]
        for link in cat_link:
            if "href" in link.attrs:
                link_cat = "http://books.toscrape.com/" + link.attrs["href"]
                get_categorie_info(link_cat)

get_all_categorie("http://books.toscrape.com/index.html")
