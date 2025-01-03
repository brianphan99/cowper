from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_html(url, triggerElement):
    """
    Scrapes the HTML content of a given URL and returns it as a string.

    Parameters:
    - url: The URL of the webpage to scrape.
    - triggerElement: Wait for this element to load before getting the page

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

        # Open the page with Selenium
        driver.get(url)

        # Use an explicit wait to wait for a specific element to be loaded
        try:
            # Wait for up to 10 seconds for the element to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, triggerElement))
            )
        except Exception as e:
            print("Error: Element not found within the time limit")
            driver.quit()
            return None

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
