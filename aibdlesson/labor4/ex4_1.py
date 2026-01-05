import requests
import urllib3
import csv
from bs4 import BeautifulSoup
import time
import random

urllib3.disable_warnings()

# 豆瓣小说页面可能有多个URL格式，尝试这个
url = "https://book.douban.com/tag/小说"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://book.douban.com/",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1"
}

# 添加延迟，避免请求过快
time.sleep(random.uniform(1, 3))

try:
    response = requests.get(url, headers=headers, verify=False, timeout=15)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容长度: {len(response.text)}")

    # 检查是否被重定向或返回错误页面
    if response.status_code != 200:
        print(f"错误: 状态码 {response.status_code}")
        exit()

    # 保存HTML到文件以便查看
    with open("douban_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("页面已保存到 douban_page.html，请查看是否有书籍信息")

    soup = BeautifulSoup(response.text, "html.parser")

    # 豆瓣书籍页面可能使用不同的类名
    # 尝试多种可能的类名选择器
    books = soup.find_all("li", class_="subject-item")
    if not books:
        books = soup.find_all("div", class_="info")
    if not books:
        books = soup.find_all("div", class_="doulist-item")

    print(f"找到 {len(books)} 个可能的书籍元素")

    # 如果没有找到，尝试另一种选择器 - 直接查找所有包含书籍信息的元素
    if not books:
        # 查看页面结构
        print("尝试分析页面结构...")
        # 打印前2000字符查看页面内容
        print("页面前2000字符:", response.text[:2000])

        # 尝试查找所有链接到书籍详情页的链接
        book_links = soup.find_all("a", href=lambda x: x and "/subject/" in x)
        print(f"找到 {len(book_links)} 个书籍链接")

        for link in book_links[:5]:
            print(f"链接: {link.get('href')}")
            parent = link.parent
            # 向上查找可能的书籍信息
            for i in range(3):
                parent = parent.parent if parent else None
                if parent:
                    print(f"父级 {i + 1}: {parent.name} class={parent.get('class')}")

    # 继续尝试其他可能的类名
    if not books:
        books = soup.select(".subject-list .subject-item")

    if not books:
        books = soup.select(".article .subject-item")

    if not books:
        # 最后尝试：查找所有可能有书籍信息的div
        all_divs = soup.find_all("div")
        for div in all_divs[:20]:  # 只检查前20个
            if div.find("h2") or div.find("a", href=lambda x: x and "/subject/" in x):
                print(f"可能的书籍容器: {div.name} class={div.get('class')}")

    book_list = []

    if books:
        print("小说详细信息：")
        for book in books[:9]:  # 只处理前9个
            # 尝试多种方式提取标题
            title = ""
            title_elem = book.find("h2")
            if title_elem:
                title = title_elem.text.strip().replace("\n", "").replace(" ", "")
            else:
                # 尝试查找a标签中的标题
                title_link = book.find("a", title=True)
                if title_link:
                    title = title_link.get("title", "").strip()
                else:
                    # 查找包含/subject/的链接
                    subject_link = book.find("a", href=lambda x: x and "/subject/" in x)
                    if subject_link:
                        title = subject_link.text.strip()

            if not title:
                continue  # 如果没有标题，跳过这个项目

            # 提取详细信息
            info = book.find("div", class_="pub")
            if not info:
                info = book.find("div", class_="author")

            author = publisher = date = price = ""

            if info:
                info_text = info.text.strip()
                info_list = [item.strip() for item in info_text.split("/")]

                if len(info_list) >= 1:
                    author = info_list[0]
                if len(info_list) >= 3:
                    publisher = info_list[-3]
                if len(info_list) >= 2:
                    date = info_list[-2]
                if len(info_list) >= 1:
                    price = info_list[-1]

            print(f"{title} | {author} | {publisher} | {date} | {price}")

            book_list.append([title, author, publisher, date, price])

        if book_list:
            # 保存到CSV文件
            with open("pachong_136.csv", "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["书名", "作者", "出版社", "出版日期", "价格"])
                writer.writerows(book_list)

            print(f"\n成功提取 {len(book_list)} 本书的信息")
            print("数据已保存到 pachong_136.csv")
        else:
            print("虽然找到了书籍元素，但未能提取到有效信息")
    else:
        print("未找到书籍信息，页面结构可能已改变")
        print("建议：")
        print("1. 打开浏览器访问: https://book.douban.com/tag/小说")
        print("2. 查看页面源代码，搜索'subject-item'或类似类名")
        print("3. 或者尝试使用Selenium模拟浏览器")

except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")