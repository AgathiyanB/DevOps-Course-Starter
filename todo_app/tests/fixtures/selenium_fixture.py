from selenium import webdriver
import pytest

@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver