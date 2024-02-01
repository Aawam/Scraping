    for url in product_urls:
        soup = get_html(url)
        scrape_result = scrape_product(soup)
        scrape.append(scrape_result)