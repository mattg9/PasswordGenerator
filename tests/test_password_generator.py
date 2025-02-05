import pytest
from playwright.sync_api import sync_playwright
from subprocess import Popen
import time

# Start the Flask app before running tests
@pytest.fixture(scope="module", autouse=True)
def start_flask_app():
    flask_process = Popen(["flask", "run"])
    time.sleep(2)  # Wait for the server to start
    yield
    flask_process.terminate()  # Terminate Flask process after tests

# Base URL of the app
BASE_URL = "http://127.0.0.1:5000"

# Helper function to extract generated password
def extract_password(page):
    return page.locator(".password").text_content()

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="module")
def page(browser):
    context = browser.new_context(
        permissions=["clipboard-read", "clipboard-write"]
    )
    page = context.new_page()
    yield page
    page.close()

# Playwright tests
@pytest.mark.parametrize(
    "use_numbers, use_punctuation, expected_chars",
    [
        (False, False, "letters"),  # Letters only
        (True, False, "letters and numbers"),  # Letters and numbers
        (False, True, "letters and punctuation"),  # Letters and punctuation
        (True, True, "all characters"),  # All characters
    ],
)
def test_password_generation(page, use_numbers, use_punctuation, expected_chars):
    page.goto(BASE_URL)
    
    # Set password options
    if use_numbers:
        page.check("input[name='include_punctuation']")
    else:
        page.uncheck("input[name='include_punctuation']")

    if use_punctuation:
        page.check("input[name='include_punctuation']")
    else:
        page.uncheck("input[name='include_punctuation']")

    # Submit form
    page.click("button[type='submit']")

    # Extract the generated password
    password = extract_password(page)
    assert password, "Password should be generated"

    # Validate password based on the selected options
    if expected_chars == "letters":
        assert all(c.isalpha() for c in password), "Password contains invalid characters"
    elif expected_chars == "letters and numbers":
        assert all(c.isalnum() for c in password), "Password contains invalid characters"
    elif expected_chars == "letters and punctuation":
        assert all(c.isalpha() or not c.isalnum() for c in password), "Password contains invalid characters"
    elif expected_chars == "all characters":
        assert all(c.isalpha() or c.isdigit() or not c.isalnum() for c in password), "Password contains invalid characters"

def test_copy_to_clipboard(page):
    page.goto(BASE_URL)
    # Submit form to generate a password
    page.click("button[type='submit']")
    password = extract_password(page)
    assert password, "Password should be generated"

    # Simulate copy to clipboard (add copy button functionality in app if needed)
    page.evaluate("""navigator.clipboard.writeText(document.querySelector('.password').textContent);""")

    # Retrieve clipboard content and verify
    clipboard_content = page.evaluate("navigator.clipboard.readText()")
    assert clipboard_content == password, "Clipboard content should match the generated password"
