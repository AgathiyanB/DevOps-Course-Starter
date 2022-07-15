from fixtures.selenium_fixture import driver
from fixtures.trello_fixture import app_with_temp_board
from time import sleep

def make_post(driver, title, desc, date):
    title_element = driver.find_element('id','item-title')
    desc_element = driver.find_element('id', 'item-desc')
    date_element = driver.find_element('id', 'due-date')
    title_element.send_keys(title)
    desc_element.send_keys(desc)
    date_element.send_keys(date)
    submit_button = driver.find_element('id', 'submit-task')
    submit_button.click()


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    make_post(driver, 'title', 'desc', '02032002')

    post_status = driver.find_element('xpath', '/html/body/div/div[2]/div/ul/li/div[2]/div/span').text

    assert post_status == 'To Do'

    dropdown = driver.find_element('xpath', '/html/body/div/div[2]/div/ul[1]/li[1]/div[2]/div/form[1]/div/button')
    dropdown.click()
    change_status_to_done_button = driver.find_element('xpath', '/html/body/div/div[2]/div/ul[1]/li[1]/div[2]/div/form[1]/div/ul/li[2]/button')
    change_status_to_done_button.click()

    new_post_status = driver.find_element('xpath', '/html/body/div/div[2]/div/ul/li/div[2]/div/span').text

    assert new_post_status == "Done"





