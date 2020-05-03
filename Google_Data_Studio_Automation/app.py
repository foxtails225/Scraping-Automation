from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

gmail = {'email': 'orijin.io.tech@gmail.com', 'password': 'nt8PHLhdYnkA'}
url = 'https://datastudio.google.com/u/0/reporting/1FRfEGOWfg-vuNI0CR9UEE-svJVCW6kZB/page/gtY7/edit'

add_field_dict_activity = {
    0: {'field_name': 'Weight (Lb)', 'field_id': 'weight_lb', 'field_round': 'ROUND(propWeightAfter*2.20462, 0)'},
    1: {'field_name': 'price per kilo', 'field_id': 'price_per_kilo',
        'field_round': 'ROUND( propMoneyAmount/propWeightAfter, 2)'}
}

add_field_dict_prodlots = {
    0: {'field_name': 'price per kilo', 'field_id': 'price_per_kilo',
        'field_round': 'ROUND( propMoneyAmount/propWeightAfter, 2)'},
    1: {'field_name': 'Weight (Lb)', 'field_id': 'weight_lb', 'field_round': 'ROUND(propWeightAfter*2.20462, 0)'},
    2: {
        'field_name': 'state (En)',
        'field_id': 'state_translated_EN',
        'field_translate_en':
            '''CASE\n\rWHEN stateCurrent = "COLLECTION_STARTED" THEN "Collection Started"\n\rWHEN stateCurrent = "COLLECTING" THEN "Collecting"\n\rWHEN stateCurrent = "COLLECTION_FINISHED" THEN "Collection Finished"\n\rWHEN stateCurrent = "FLOATERSSEPARATED" THEN "Floaters Separated"\n\rWHEN stateCurrent = "DEPULPED" THEN "Depulped"\n\rWHEN stateCurrent = "INFERMENTATION" THEN "In fermentation"\n\rWHEN stateCurrent = "WASHED" THEN "Washed"\n\rWHEN stateCurrent = "DRYING" THEN "Drying"\n\rWHEN stateCurrent = "BAGGED" THEN "Bagged"\n\rWHEN stateCurrent = "CLEANED" THEN "Cleaned"\n\rWHEN stateCurrent = "CLASSIFIED" THEN "Classified"\n\rWHEN stateCurrent = "ROASTED" THEN "Roasted"\n\rWHEN stateCurrent = "WINNOWED" THEN "Winnowed"\n\rWHEN stateCurrent = "GRINDED" THEN "Grinded"\n\rWHEN stateCurrent = "CONCHED" THEN "Conched"\n\rWHEN stateCurrent = "TEMPERED" THEN "tempering"\n\rWHEN stateCurrent = "MOLDED" THEN "molding"\n\rWHEN stateCurrent = "COLLECTED" THEN "Collected"\n\rWHEN stateCurrent = "HARVESTED" THEN "Harvested"\n\rWHEN stateCurrent = "FERMENTED" THEN "Fermented"\n\rWHEN stateCurrent = "DRIED" THEN "Dried"\n\rWHEN stateCurrent = "Open" THEN "Open"\n\rWHEN stateCurrent = "Public" THEN "Public"\n\rWHEN stateCurrent = "Origin" THEN "Origin"\n\rWHEN stateCurrent = "Private" THEN "Private"\n\rWHEN stateCurrent = "EndProduct" THEN "EndProduct"\n\rWHEN stateCurrent = "Closed" THEN "Closed"\n\rELSE\n\r"Other"\n\rEND'''
    },
    3: {
        'field_name': 'state (ES)',
        'field_id': 'state_translated_ES',
        'field_translate_es':
            '''CASE\n\rWHEN stateCurrent = "COLLECTION_STARTED" THEN "Cosecha Iniciada"\n\rWHEN stateCurrent = "COLLECTING" THEN "En Cosecha"\n\rWHEN stateCurrent = "COLLECTION_FINISHED" THEN "Cosecha Finalizada"\n\rWHEN stateCurrent = "FLOATERSSEPARATED" THEN "Flotadores Separados"\n\rWHEN stateCurrent = "DEPULPED" THEN "Despulpado"\n\rWHEN stateCurrent = "INFERMENTATION" THEN "En Fermentación"\n\rWHEN stateCurrent = "WASHED" THEN "Lavado"\n\rWHEN stateCurrent = "DRYING" THEN "Secando"\n\rWHEN stateCurrent = "BAGGED" THEN "Ensacado"\n\rWHEN stateCurrent = "CLEANED" THEN "Limpiado"\n\rWHEN stateCurrent = "CLASSIFIED" THEN "clasificado de grano"\n\rWHEN stateCurrent = "ROASTED" THEN "Tostado"\n\rWHEN stateCurrent = "WINNOWED" THEN "Descascarillado"\n\rWHEN stateCurrent = "GRINDED" THEN "Molienda"\n\rWHEN stateCurrent = "CONCHED" THEN "Conchado"\n\rWHEN stateCurrent = "TEMPERED" THEN "Temperado"\n\rWHEN stateCurrent = "MOLDED" THEN "Moldeado"\n\rWHEN stateCurrent = "COLLECTED" THEN "Acopio"\n\rWHEN stateCurrent = "HARVESTED" THEN "Cosecha"\n\rWHEN stateCurrent = "FERMENTED" THEN "Fermentación"\n\rWHEN stateCurrent = "DRIED" THEN "Secando"\n\rWHEN stateCurrent = "Open" THEN "Abierto"\n\rWHEN stateCurrent = "Public" THEN "Público"\n\rWHEN stateCurrent = "Origin" THEN "Origen"\n\rWHEN stateCurrent = "Private" THEN "Privada"\n\rWHEN stateCurrent = "EndProduct" THEN "Producto final"\n\rWHEN stateCurrent = "Closed" THEN "Cerrada"\n\rELSE\n\r"Other"\n\rEND'''
    },
    4: {
        'field_name': 'process',
        'field_id': 'workflow_Translated',
        'field_process':
            '''CASE\n\rWHEN workFlowId = "honeyCoffee" THEN "Honey"\n\rWHEN workFlowId = "washedCoffee" THEN "Washed"\n\rWHEN workFlowId = "naturalCoffee" THEN "Natural"\n\rELSE\n\r"Other"\n\rEND'''
    },
}


def check_exists(element):
    try:
        driver.find_element_by_css_selector(element)
    except NoSuchElementException:
        return False
    return True


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=chrome")

with webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options) as driver:
    driver.maximize_window()

    driver.get(url)

    # if check_exists("._md.md-data-studio-theme.md-transition-in"):
    time.sleep(7)
    if check_exists("._md.md-data-studio-theme.md-transition-in"):
        driver.get("https://myaccount.google.com/intro")
        wait = WebDriverWait(driver, 3)

        if driver.find_elements_by_css_selector(".gb_4.gb_5.gb_ge.gb_wb"):
            sign_button = driver.find_element_by_css_selector(".gb_4.gb_5.gb_ge.gb_wb")
            sign_button.click()
            email = driver.find_element_by_css_selector("[type='email']")
            email.clear()
            email.click()
            email.send_keys(gmail['email'])
            email_button = driver.find_element_by_id("identifierNext")
            email_button.click()

            wait = WebDriverWait(driver, 10)
            wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "[type='password']")))
            password = driver.find_element_by_css_selector("[type='password']")
            password.clear()
            password.click()
            password.send_keys(gmail['password']);
            pass_button = driver.find_element_by_id("passwordNext")
            pass_button.click()
            wait = WebDriverWait(driver, 1000)
            wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#gb")))
            driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.mat-menu-trigger.mat-button.mat-button-base.ng-star-inserted:first-child")))
    file_click = driver.find_element_by_css_selector(
        "button.mat-menu-trigger.mat-button.mat-button-base.ng-star-inserted:first-child")
    file_click.click()

    time.sleep(3)
    file_copy = driver.find_element_by_css_selector(".menu-item-container.ng-star-inserted:nth-child(10)>button")
    file_copy.click()

    time.sleep(3)
    select_new_datasource = driver.find_elements_by_css_selector(".datasourceItem>md-select")
    select_new_datasource[0].click()

    time.sleep(3)
    create_new_datasource = driver.find_elements_by_css_selector("div.datasourcePickerCreate")
    create_new_datasource[1].click()

    time.sleep(3)
    select_big_query = driver.find_elements_by_css_selector(
        "button.select.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
    select_big_query[3].click()

    time.sleep(3)
    select_project = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row")
    for i in range(len(select_project)):
        if select_project[i].text == "orijin-dev":
            select_project[i].click()
            break

    time.sleep(3)
    select_dataset = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row")

    for i in range(len(select_dataset)):
        if select_dataset[i].text == "demo_coffee_salla_bq3":
            select_dataset[i].click()
            break

    time.sleep(3)
    select_table = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row .display-property.ellipsis-overflow.ng-binding")

    for i in range(len(select_table)):
        if select_table[i].text == "activitycompletions":
            select_table[i].click()
            break

    time.sleep(2)
    connect_button = driver.find_element_by_css_selector(
        "button.connect.md-accent.md-raised.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
    connect_button.click()

    for i in range(len(add_field_dict_activity)):
        time.sleep(5)
        add_field_button = driver.find_elements_by_css_selector(".create-field-button-container.layout-row>button")
        add_field_button[1].click()

        time.sleep(2)
        field_name = driver.find_elements_by_css_selector(".ng-valid.md-input")
        field_name[2].clear()
        field_name[2].click()
        field_name[2].send_keys(add_field_dict_activity[i]['field_name'])

        field_id = driver.find_elements_by_css_selector(".ng-valid.md-input")
        field_id[3].clear()
        field_id[3].click()
        field_id[3].send_keys(add_field_dict_activity[i]['field_id'])

        context = driver.find_element_by_css_selector('.CodeMirror-cursor')
        action = ActionChains(driver)
        action.move_to_element(context).click().send_keys(add_field_dict_activity[i]['field_round']).perform()

        time.sleep(3)
        save_button = driver.find_elements_by_css_selector(
            ".md-accent.md-raised.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
        save_button[1].click()

        time.sleep(5)
        back_button = driver.find_elements_by_css_selector(".arrow-label.ng-binding.ng-scope")
        back_button[0].click()

    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, ".done")))
    report_button = driver.find_element_by_css_selector(".done")
    report_button.click()

    time.sleep(3)
    select_new_datasource = driver.find_elements_by_css_selector(".datasourceItem>md-select")
    select_new_datasource[1].click()

    time.sleep(3)
    create_new_datasource = driver.find_elements_by_css_selector("div.datasourcePickerCreate")
    create_new_datasource[1].click()

    time.sleep(3)
    select_big_query = driver.find_elements_by_css_selector(
        "button.select.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
    select_big_query[3].click()

    time.sleep(3)
    select_project = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row")
    for i in range(len(select_project)):
        if select_project[i].text == "orijin-dev":
            select_project[i].click()
            break

    time.sleep(3)
    select_dataset = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row")

    for i in range(len(select_dataset)):
        if select_dataset[i].text == "demo_coffee_salla_bq3":
            select_dataset[i].click()
            break

    time.sleep(3)
    select_table = driver.find_elements_by_css_selector(
        "div.list.flex button.list-option.ellipsis-overflow.md-button.md-data-studio-theme.md-ink-ripple.layout-row .display-property.ellipsis-overflow.ng-binding")

    for i in range(len(select_table)):
        if select_table[i].text == "prodlots":
            select_table[i].click()
            break

    wait = WebDriverWait(driver, 2)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.connect.md-accent.md-raised.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")))
    connect_button = driver.find_element_by_css_selector(
        "button.connect.md-accent.md-raised.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
    connect_button.click()

    for i in range(len(add_field_dict_prodlots)):
        wait = WebDriverWait(driver, 5000)
        wait.until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, ".create-field-text")))
        add_field_button = driver.find_element_by_css_selector(".create-field-text")
        add_field_button.click()

        time.sleep(2)
        field_name = driver.find_elements_by_css_selector(".ng-valid.md-input")
        field_name[2].clear()
        field_name[2].click()
        field_name[2].send_keys(add_field_dict_prodlots[i]['field_name'])

        field_id = driver.find_elements_by_css_selector(".ng-valid.md-input")
        field_id[3].clear()
        field_id[3].click()
        field_id[3].send_keys(add_field_dict_prodlots[i]['field_id'])

        context = driver.find_element_by_css_selector('.CodeMirror-cursor')
        action = ActionChains(driver)

        if i == 2:
            action.move_to_element(context).click().send_keys(
                add_field_dict_prodlots[i]['field_translate_en']).perform()
        elif i == 3:
            action.move_to_element(context).click().send_keys(
                add_field_dict_prodlots[i]['field_translate_es']).perform()
        elif i == 4:
            action.move_to_element(context).click().send_keys(add_field_dict_prodlots[i]['field_process']).perform()
        elif i == 0 or i == 1:
            action.move_to_element(context).click().send_keys(add_field_dict_prodlots[i]['field_round']).perform()

        time.sleep(7)
        save_button = driver.find_elements_by_css_selector(
            ".md-accent.md-raised.md-button.ng-scope.md-data-studio-theme.md-ink-ripple")
        save_button[1].click()

        time.sleep(7)
        back_button = driver.find_elements_by_css_selector(".arrow-label.ng-binding.ng-scope")
        back_button[0].click()

    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, ".done")))
    report_button = driver.find_element_by_css_selector(".done")
    report_button.click()

    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CSS_SELECTOR, ".md-accent.md-raised.md-button.md-data-studio-theme.md-button.md-ink-ripple")))
    make_report = driver.find_element_by_css_selector(
        ".md-accent.md-raised.md-button.md-data-studio-theme.md-button.md-ink-ripple")
    make_report.click()

    wait = WebDriverWait(driver, 50)
    first_result = wait.until(presence_of_element_located((By.CSS_SELECTOR, "h3>div")))
