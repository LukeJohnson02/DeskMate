import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ARTIFACT_DIR = os.getenv("E2E_ARTIFACT_DIR", "e2e-artifacts")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture()
def browser(request):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1000")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(1)
    yield driver
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        test_name = request.node.name
        driver.save_screenshot(os.path.join(ARTIFACT_DIR, f"{test_name}.png"))
        with open(
            os.path.join(ARTIFACT_DIR, f"{test_name}.html"),
            "w",
            encoding="utf-8",
        ) as page_file:
            page_file.write(driver.page_source)
    driver.quit()


def wait_for(browser, timeout=15):
    return WebDriverWait(browser, timeout)


def by_test_id(test_id):
    return (By.CSS_SELECTOR, f'[data-testid="{test_id}"]')


def selected_category_value(driver):
    return driver.find_element(*by_test_id("ticket-category")).get_attribute("value")


def open_login(browser):
    browser.get(FRONTEND_URL)
    browser.execute_script("window.localStorage.clear();")
    browser.get(FRONTEND_URL)
    wait_for(browser).until(EC.visibility_of_element_located(by_test_id("login-form")))


def login(browser, email, password):
    open_login(browser)
    browser.find_element(*by_test_id("login-email")).send_keys(email)
    browser.find_element(*by_test_id("login-password")).send_keys(password)
    browser.find_element(*by_test_id("login-submit")).click()
    wait_for(browser).until(
        EC.visibility_of_element_located(by_test_id("dashboard-page"))
    )


def test_login_page_renders(browser):
    open_login(browser)

    assert "Welcome to DeskMate" in browser.page_source
    assert browser.find_element(*by_test_id("login-email")).is_displayed()
    assert browser.find_element(*by_test_id("login-password")).is_displayed()


def test_invalid_login_shows_error(browser):
    open_login(browser)

    browser.find_element(*by_test_id("login-email")).send_keys("user1@example.com")
    browser.find_element(*by_test_id("login-password")).send_keys("wrong-password")
    browser.find_element(*by_test_id("login-submit")).click()

    wait_for(browser).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Invalid email or password",
        )
    )


def test_user_can_login_and_view_dashboard(browser):
    login(browser, "user1@example.com", "password123")

    wait_for(browser).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "My Support Tickets")
    )
    assert "Signed in as user1 (user)" in browser.page_source
    assert "Raise a Ticket" in browser.page_source


def test_user_can_create_ticket(browser):
    login(browser, "user1@example.com", "password123")
    ticket_title = f"Selenium ticket {int(time.time())}"

    wait_for(browser).until(EC.element_to_be_clickable(by_test_id("ticket-title")))
    wait_for(browser).until(lambda driver: len(category_select(driver).options) > 0)
    category_id = wait_for(browser).until(
        lambda driver: selected_category_value(driver)
    )
    browser.find_element(*by_test_id("ticket-title")).send_keys(ticket_title)
    category_select(browser).select_by_value(category_id)
    browser.find_element(*by_test_id("ticket-description")).send_keys(
        "Created by the Selenium end-to-end test suite."
    )
    wait_for(browser).until(EC.element_to_be_clickable(by_test_id("ticket-submit")))
    browser.find_element(*by_test_id("ticket-submit")).click()

    wait_for(browser).until(
        lambda driver: (
            "Ticket created successfully." in driver.page_source
            or ticket_title in driver.page_source
            or "Could not create the ticket" in driver.page_source
        )
    )
    page_source = browser.page_source
    assert "Could not create the ticket" not in page_source
    assert "Ticket created successfully." in page_source or ticket_title in page_source


def category_select(driver):
    return Select(driver.find_element(*by_test_id("ticket-category")))


def test_logout_returns_to_login(browser):
    login(browser, "user1@example.com", "password123")

    logout_button = wait_for(browser).until(
        EC.element_to_be_clickable(by_test_id("logout-button"))
    )
    logout_button.click()

    wait_for(browser).until(
        lambda driver: driver.execute_script(
            "return window.localStorage.getItem('token')"
        )
        is None
    )
    wait_for(browser).until(
        lambda driver: driver.current_url.rstrip("/") == FRONTEND_URL.rstrip("/")
    )
    wait_for(browser).until(EC.visibility_of_element_located(by_test_id("login-form")))


def test_admin_can_move_open_ticket_into_progress(browser):
    login(browser, "admin1@example.com", "adminpass123")

    wait_for(browser).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Ticket Triage")
    )
    start_button = wait_for(browser).until(
        EC.element_to_be_clickable(by_test_id("start-work-button"))
    )
    start_button.click()

    wait_for(browser).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Ticket moved to in progress.",
        )
    )
