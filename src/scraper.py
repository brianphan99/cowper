from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_html(url, delay=5):
    """
    Scrapes the HTML content of a given URL and returns it as a string.

    Parameters:
    - url: The URL of the webpage to scrape.
    - delay: Time in seconds to wait for the page to load. Defaults to 5 seconds.

    Returns:
    - A string containing the prettified HTML content of the page.
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode for server

    try:
        # Set up the Selenium WebDriver with options
        driver = webdriver.Chrome(options=chrome_options)

        # ladbrokes only shows odds when window size is big
        driver.set_window_size(1920, 1080)
        # set implicit wait time
        driver.implicitly_wait(10)

        # Open the page with Selenium
        driver.get(url)

        # Add a delay to allow the page to load
        time.sleep(delay)

        # Get the page source after JavaScript has executed
        html = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Return the HTML soup
        return soup

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Close the browser
        driver.quit()
