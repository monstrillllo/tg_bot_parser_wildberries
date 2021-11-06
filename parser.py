import typing

import requests
from bs4 import BeautifulSoup
import sqlite3


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
}


async def get_page(url: str) -> str:
    """
    Return src of url page
    :param url: str, site url
    :return: str, page src
    """
    session = requests.Session()
    response = session.get(url, headers=headers)
    return response.text


async def get_brand(url: str) -> str:
    """
    Return brand of product from wildberries
    :param url: str, product page url
    :return: str, product brand
    """
    src = await get_page(url)
    soup = BeautifulSoup(src, 'lxml')
    brand = soup.find("div", class_="main__container").find("div", {'id': 'app'}).\
        find("div", {"itemtype": "http://schema.org/Product"}).find("meta", {"itemprop": "brand"}).get('content')
    return brand


async def get_title(url: str) -> str:
    """
    Return title of product from wildberries
    :param url: str, product page url
    :return: str, product title
    """
    src = await get_page(url)
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find("div", class_="main__container").find("div", {'id': 'app'}).\
        find("div", {"itemtype": "http://schema.org/Product"}).find("meta", {"itemprop": "name"}).get('content')
    return name


def get_cursor() -> sqlite3.Cursor:
    """
    Connect to sqlite brands_titles.db
    :return: sqlite3.Cursor, connection cursor
    """
    conn = sqlite3.connect("brands_titles.db")
    cursor = conn.cursor()
    return cursor


def write_brand_db(article: str, brand: str) -> None:
    """
    Write article and brand to db
    :param article: str, product article
    :param brand: str, product brand
    :return: None
    """
    cursor = get_cursor()
    cursor.execute("""
        create table if not exists article_brand(
        article int primary key,
        brand text
        )
    """)
    insert_row = "insert into article_brand values ('{article}', '{brand}') " \
                 "on conflict(article) do update set brand='{brand}' where article='{article}'"\
        .format(article=article, brand=brand)
    cursor.execute(insert_row)
    cursor.connection.commit()
    cursor.close()


def write_title_db(article: str, title: str) -> None:
    """
    Write article and title to db
    :param article: str, product article
    :param title: str, product title
    :return: None
    """
    cursor = get_cursor()
    cursor.execute("""
        create table if not exists article_title(
        article int primary key,
        title text
        )
    """)
    insert_row = "insert into article_title values ('{article}', '{title}') " \
                 "on conflict(article) do update set title='{title}' where article='{article}'"\
        .format(article=article, title=title)
    cursor.execute(insert_row)
    cursor.connection.commit()
    cursor.close()


async def select_title_db(article: str) -> typing.Optional[str]:
    """
    Select title by article from db
    :param article: str, product article
    :return: str|None, product title or None if product doesnt exist in db
    """
    try:
        cursor = get_cursor()
        cursor.execute("""
            select title from article_title where article='{article}'
        """.format(article=article))
        result = cursor.fetchone()
        cursor.close()
        return result
    except:
        return None


async def select_brand_db(article: str) -> typing.Optional[str]:
    """
    Select brand by article from db
    :param article: str, product article
    :return: str|None, product brand or None if product doesnt exist in db
    """
    try:
        cursor = get_cursor()
        cursor.execute("""
            select brand from article_brand where article='{article}'
        """.format(article=article))
        result = cursor.fetchone()
        cursor.close()
        return result
    except:
        return None


def main():
    # print(type(get_brand('https://www.wildberries.ru/catalog/38567378/detail.aspx')))
    # print(get_title('https://www.wildberries.ru/catalog/38567378/detail.aspx'))
    # write_brand_db('31321', 'lol')
    write_title_db('4324', 'lololololol')


if __name__ == '__main__':
    main()
