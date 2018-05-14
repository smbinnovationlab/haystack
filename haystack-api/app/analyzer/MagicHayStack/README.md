- External Usage:
    ```Python
    from MagicHayStack import get_price
    l = get_price(page_url, image_urls)
    for price, currency, confidence in l:
        # Do something...
    ```
    Or, in parrallel
    ```Python
    from MagicHayStack import parallel_get_price
    l = parallel_get_price(page_urls, image_urls)
    for result in l:
        for price, currency, confidence in result:
            # Do something...
    ```
    To submit labelled webpage
    ```Python
    from MagicHayStack import submit_label
    submit_label(19.99, 'a.com', None | ['b.jpg'], 'record.csv')
    ```

- Introduction
    - Extract price from any eCommerce web page

- Requirements:
    - Make sure to have installed one of the web drivers (e.g. ChromeDriver, PhantomJS).
    - Dependence: numpy, sklearn, selenium, BeautifulSoup4, <del>xgboost</del>

- Usage:
    - data_generation.py for collecting data
    - script.py for experimental code

