import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up logging (same as before)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_execution.log")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Define a fixture to set up warning filters
@pytest.fixture(autouse=True)
def _handle_warnings():
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message="urllib3 (.*) or chardet (.*)/charset_normalizer (.*) doesn't match a supported version!")

@pytest.mark.parametrize("button_text", ["Catalogs", "Profiles", "Other"])
def test_scrape_regscale_catalogs(driver, button_text):
    # Log browser information
    browser_name = driver.capabilities['browserName']
    browser_version = driver.capabilities.get('browserVersion') or driver.capabilities.get('version')
    logger.info(f"Running test with browser: {browser_name} (version: {browser_version})")

    logger.info(f"Starting test with button_text: {button_text}")
    driver.get("https://regscale.com")
    
    try:
        # Navigate to Resources / Catalogs and Profiles
        resources_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Resources"))
        )
        resources_menu.click()
        logger.info("Clicked on Resources menu")
        
        catalogs_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Catalogs and Profiles"))
        )
        catalogs_link.click()
        logger.info("Clicked on Catalogs and Profiles link")
        
        # Click on the specified button using partial text match
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
        )
        button.click()
        logger.info(f"Clicked on {button_text} button")
        
        cards = []
        page = 1
        
        while True:
            # Wait for cards to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "catalog-card"))
            )
            
            # Collect card information
            card_elements = driver.find_elements(By.CLASS_NAME, "catalog-card")
            for card in card_elements:
                card_type = card.find_element(By.CLASS_NAME, "type").text
                card_name = card.find_element(By.CLASS_NAME, "title").text
                cards.append({"type": card_type, "name": card_name})
            
            logger.info(f"Collected {len(card_elements)} cards from page {page}")
            
            # Check if there's a next page
            try:
                next_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "next-btn"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                page += 1
                # Wait for the page to load after clicking next
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(card_elements[0])
                )
            except TimeoutException:
                logger.info("No more pages to load")
                break
        
        # Verify each card has a type and a name
        for card in cards:
            assert card["type"], f"Card missing type: {card}"
            assert card["name"], f"Card missing name: {card}"
        
        logger.info(f"Total cards collected: {len(cards)}")
        
        # Assert that we have collected some cards
        assert len(cards) > 0, f"No cards were collected for {button_text}"
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

# Make sure to close the handlers after the test
@pytest.fixture(scope="module", autouse=True)
def close_handlers():
    yield
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)