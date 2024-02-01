import requests
from bs4 import BeautifulSoup
import pandas as pd #gunakan library pandas

def get_html(url : str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def get_max_page(soup : BeautifulSoup) -> None:
    max_page : list[BeautifulSoup] = soup.find("ul", class_="pagination").find_all("li", class_="page-item")
    
    return int(max_page[-1].find("a").get_text())

def get_products_items(soup):
    item_products : list[BeautifulSoup] = soup.find_all("div", "o_wsale_product_grid_wrapper position-relative h-100")
    urls = [f'https://www.bhinneka.com{url.find("a")["href"]}' for url in item_products]

    item = []

    for url in urls:
        if not any(keyword in url for keyword in ["for", "cable", "case", "wallet", "glass", "charger", "power", "leather", "fast", "ringke"]):
            item.append(url)

    return item

"""
def parsing(item_products): #Outside Link
    output = []
    for product in item_products:
        nama = product.find('a', 'text-primary text-decoration-none').get_text()
        harga = product.find('span','oe_currency_value').get_text().replace("Rp","").replace(".", "").replace(" ", "")
        installment = product.find('span', class_ = "bmd-installment").get_text().replace("Cicilan Rp. ", "").replace("/bln", "").replace(".", "")
        location = product.find('div', class_ = "o_wsale_product_sub d-flex justify-content-between align-items-end pb-1").find('div', class_ = "d-flex flex-column").find('span', class_ = "bmd-installment").get_text().replace("\n", "").replace(" ","") # -> None.get_text()
        url = product.find('a', 'text-primary text-decoration-none')['href'].replace(" ", "")
        final_url = (f"https://www.bhinneka.com/{url}")
        out = {"Name" : nama, "Price" : harga, "Installment" : installment, "Location" : location, "URL" : final_url}
        output.append(out)
    return output
"""

def scrape_product(soup: BeautifulSoup): #Inside Link

    title_element = soup.find("div", id="product_details").find("h1")
    title = title_element.get_text() if title_element else None
    price = soup.find("div", id="o_wsale_cta_wrapper").find("div", class_="css_quantity input-group d-inline-flex me-2 mb-2 align-middle input-group-lg").find("span", id="priceSubtotalWrapper").get_text().replace("Total Rp","").replace("\xa0","")
    
    out = [title,price]
    return out

if __name__ == "__main__":
    product_urls = []
    scrape = []
    soup = get_html("https://www.bhinneka.com/jual?page=1&cari=iphone&order=")
    max_page = get_max_page(soup)

    for i in range(1, max_page + 1):
        sop = get_html(f"https://www.bhinneka.com/jual?page={i}&cari=iphone&order=")
        urls = get_products_items(sop)
        product_urls.extend(urls)

    print(product_urls)
    print(len(product_urls))
        
    for url in product_urls:
        soup = get_html(url)
        scrape_result = scrape_product(soup)
        scrape.append(scrape_result)
    
    print(scrape)
    print(len(scrape))

