# Web Scraping Challenge: Scraping the Entire "Books to Scrape" Website

## Introduction

In our last session, we wrote a script to extract book data from a single page. Now, it's time to take your skills to the next level!

This exercise challenges you to apply and extend what you've learned to scrape the **entire** website, which contains 50 pages of book data.

**The goal of this exercise is to build your problem-solving and debugging skills.** Before you ask for help or search for a solution, try to figure out the challenges on your own. Learning to debug is one of the most important skills you will develop as a programmer.

---

## Your Challenge: Scrape All 50 Pages

Your task is to modify the initial script to scrape the **title** and **price** of every book from all 50 pages of the [Books to Scrape](http.books.toscrape.com/) website and save them into a single `books.csv` file.

### Getting Started

1.  You will find the original script from our last session in the `scraper_page_1.py` file.
2.  **Do not modify this file.** Instead, create a copy and name it `scraper_all_pages.py`. You will work in this new file.
3.  Your goal is to modify `scraper_all_pages.py` so that it loops through all 50 pages and collects the data.



***

### Core Functions and Attributes Cheatsheet

This table lists the most important functions and attributes you will use from the `requests`, `BeautifulSoup`, and `pandas` libraries for this project.

#### `requests` Library
*Used for fetching the web page content.*

| Function / Attribute    | Description                                                                     | Example Usage                             | [Official Documentation](https://requests.readthedocs.io/en/latest/) |
| :---------------------- | :------------------------------------------------------------------------------ | :---------------------------------------- | :------------------------------------------------------------------- |
| **`requests.get(url)`** | Sends a GET request to a URL to retrieve its content.                           | `response = requests.get(URL)`            | [Link to `get` docs](https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request) |
| **`.content`**          | The raw HTML content of the response, in bytes.                                 | `soup = BeautifulSoup(response.content)`  | [Link to `.content` docs](https://requests.readthedocs.io/en/latest/user/quickstart/#response-content) |
| **`.status_code`**      | The HTTP status code of the response. `200` means the request was successful.    | `print(response.status_code)`             | [Link to `.status_code` docs](https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes) |

---

#### `BeautifulSoup` Library
*Used for parsing and navigating the HTML content.*

| Function / Attribute             | Description                                                                                             | Example Usage                                          | [Official Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| :------------------------------- | :------------------------------------------------------------------------------------------------------ | :----------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **`BeautifulSoup(html, ...)`**   | Creates a parseable object from the raw HTML string. This is your first step.                           | `soup = BeautifulSoup(response.content, "html.parser")` | [Link to constructor docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup) |
| **`find(name, class_, ...)`**    | Returns the **first tag** that matches your criteria.                                                   | `container = soup.find(name="ol", class_="row")`       | [Link to `find` docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find) |
| **`find_all(name, class_, ...)`** | Returns a **list of all tags** that match your criteria. Perfect for looping through multiple items.      | `books = container.find_all(name="li")`                | [Link to `find_all` docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all) |
| **`.text`**                      | An attribute that gets the text content from within a tag, with all HTML tags removed.                  | `title = book.h3.a.text`                               | [Link to `.text` docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#text) |
| **`.get(attribute)`**            | Extracts the value from a tag's attribute (e.g., the `href` from a link or `src` from an image).          | `link = book.h3.a.get("href")`                         | [Link to attribute docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes) |

---

#### `pandas` Library
*Used for organizing and saving your data.*

| Function / Attribute       | Description                                                                                               | Example Usage                               | [Official Documentation](https://pandas.pydata.org/docs/) |
| :------------------------- | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------------- |
| **`pd.DataFrame(data)`**   | Creates a 2D table-like data structure (a DataFrame) from a list of dictionaries or other data types.     | `df = pd.DataFrame(data)`                   | [Link to `DataFrame` docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) |
| **`df.to_csv(filename)`**  | Writes the DataFrame to a comma-separated values (CSV) file. The `index=False` argument is highly recommended. | `df.to_csv("books.csv", index=False)`       | [Link to `to_csv` docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) |

---

## Understanding the HTML Structure (The Hierarchy)

To scrape a website effectively, you must first understand its structure. HTML documents are built like a tree, with elements nested inside other elements. This is called a parent-child hierarchy.

Let's look at the structure of the book listings on the website:

1.  All the books are contained within an ordered list (`<ol>`) tag that has the class `row`. This is our main container.

    ![OL with class row](https://i.imgur.com/nZgCgN0.png)

2.  Inside this `<ol>`, each book is an individual list item (`<li>`). So, the `<ol>` is the **parent**, and each `<li>` is a **child**. This is why we first find the `<ol>` and then find all the `<li>` elements *inside* it.

3.  Inside each `<li>`, you'll find an `<article>` tag, which contains all the information for that specific book (image, title, price, etc.).

4.  The title is located inside a link (`<a>`) tag, which is nested within a header (`<h3>`) tag.
    *   Hierarchy: `<li>` -> `<article>` -> `<h3>` -> `<a>`

5.  The price is in a paragraph (`<p>`) tag with the class `price_color`.
    *   Hierarchy: `<li>` -> `<article>` -> `<div class="product_price">` -> `<p class="price_color">`

Understanding this hierarchy allows you to navigate the HTML tree precisely with BeautifulSoup to extract the exact data you need.

---

## A Beginner's Guide to Debugging Your Scraper

When your code doesn't work, don't panic! Debugging is a normal part of programming. Here’s how you can find and fix problems in your script.

### 1. `print()` is Your Best Friend
The simplest way to check what your code is doing is to print the contents of your variables at different steps.

*   **Did the request work?** Check the status code. A `200` means success!
    ```python
    response = requests.get("https://books.toscrape.com/catalogue/page-1.html")
    print(response.status_code)
    ```
*   **Is BeautifulSoup parsing the HTML correctly?** Print a small part of the `soup` object to see the HTML structure.
    ```python
    soup = BeautifulSoup(response.content, "html.parser")
    # .prettify() makes the HTML readable
    print(soup.prettify()[:500]) # Print only the first 500 characters
    ```
*   **Are you finding the right elements?** Check if your `find` or `find_all` methods are returning anything.
    ```python
    books = soup.find_all(name="li")
    print(f"Found {len(books)} books on this page.")
    # If this prints "Found 0 books", your selector is wrong!
    ```
*   **Is your loop working?** Print the data you extract inside the loop for the first one or two items.
    ```python
    # Inside your for loop
    print(f"Title: {title}, Price: {price}")
    ```

### 2. Start Small
Don't try to scrape all 50 pages at once.
*   First, make your loop work for just **2 or 3 pages**.
*   Once you confirm that it's correctly fetching and saving data from the first few pages, then you can increase the range to all 50.

### 3. Read the Error Messages!
Python error messages can look intimidating, but they are incredibly helpful. Read them carefully.
*   They will tell you the **file name** and the **line number** where the error occurred.
*   They will give you the **type of error** (e.g., `AttributeError`, `IndexError`), which tells you what kind of problem it is. An `AttributeError: 'NoneType' object has no attribute 'a'` often means your BeautifulSoup selector failed to find an element, so the variable is `None`.

### 4. Inspect the URL
Your main challenge is to go from page to page.
*   Manually navigate the website from page 1 to page 2, then to page 3.
*   Look at the URL in your browser's address bar. What part of it changes? How can you replicate that pattern in your Python code?

---

## Documentation of Libraries and Functions

Refer to these official documentation links when you need to understand a function or discover new ones.

*   **[`requests`](https://requests.readthedocs.io/en/latest/)**: For making HTTP requests to get the webpage content.
*   **[`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)**: For parsing the HTML and navigating the data structure.
*   **[`pandas`](https://pandas.pydata.org/docs/)**: For organizing your scraped data into a structured table and saving it to a CSV file.

**Good luck, and happy scraping!**
