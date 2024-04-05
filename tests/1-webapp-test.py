from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from random import randint
import datetime
from time import sleep
import pytest


BASE_URL = "http://localhost:5000"
TASKS_URL = "/tasks"
ALL_TASKS_URL = "/all_tasks"

def test_0():
    assert True
    print("Ce test doit s'exécuter")
    with pytest.raises(ValueError):
        raise ValueError("ce test doit aussi s'exécuter")


def test_1_creation_et_completion():
    """Un test de bout en bout pour la fonctionnalité de création et validation d'une page.
    
    Spécifications (dans le désordre, à vous de les réorganiser):
    
    - Sur toutes les pages du site, vous avez un lien HTML avec la classe CSS "link-create-task".
    - Quand on clique sur le lien susmentionné, on arrive sur un formulaire HTML simple avec le fonctionnement suivant:
        - un champ de type input texte ou textarea, et avec la classe CSS "field-name"
        - un champ de type select + option avec la classe CSS "field-priority" et les valeurs possibles "low", "normal", "urgent"
        - un input de type 'submit', conçu pour valider le formulaire.
        - quand on valide le formulaire, on est redirigé à la fin vers la page contenant la liste de toutes les tâches en cours, /tasks (c'est à dire toutes les tãches pas encore complétées)
    - Une page /tasks affiche toutes les tâches pas encore complétées.
    - Une page /all_tasks affiche toutes les tâches, y compris les tâches complétées
    - Une tâche est représentée par un élément de type div avec la classe CSS task.
        - Les tâches non complétées ont en plus la classe CSS task-incomplete ...
        - tandis que les tâches accomplies ont la classe CSS task-completed
        - les tâches effacées ont la classe CSS task-deleted
        - toutes les tâches ont un bouton avec la classe CSS task-state-toggle. Quand on clique sur ce bouton:
            - une tâche non-complétée est marquée comme accomplie
            - une tâche accomplie est ramenée au statut non-complété
            - la page se recharge ensuite pour refléter le nouvel état
    """
    # Initialize the WebDriver
    # driver = webdriver.Chrome(keep_alive=True)
    try:
        driver = webdriver.Firefox()
        driver.get(f"{BASE_URL}/")
        sleep(1)
        # Find and click the link named "Create task"
        create_task_link = driver.find_element(By.CSS_SELECTOR, "a.link-create-task")
        create_task_link.click()
        sleep(1)
        # Find the input fields and fill them with appropriate values
        name_field = driver.find_element(By.CSS_SELECTOR, "form .field-name")
        # current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text_to_write = f"Test {randint(1, 100_000_000)}"
        for c in text_to_write:
            name_field.send_keys(c)
            sleep(randint(1, 100) / 500.0)
        sleep(1)
        priority_field = Select(driver.find_element(By.CSS_SELECTOR, "form select.field-priority"))
        #   Selecting a priority option from dropdown by value (you may need to adapt this based on your HTML)
        priorities = ["low", "normal", "urgent"][randint(0, 2)]
        priority_field.select_by_value(priorities)
        sleep(2)
        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

        sleep(1)
        assert driver.current_url.endswith(TASKS_URL)
        new_task_list = driver.find_elements(
            By.XPATH, f"""//*[contains(text(),'{text_to_write}')]"""
        )
        assert len(new_task_list) == 1
        new_task = new_task_list[0]
        new_task.find_element(By.CSS_SELECTOR, "button.task-state-toggle").click()
        sleep(2)
        new_task_list = driver.find_elements(
            By.XPATH, f"""//*[contains(text(),'{text_to_write}')]"""
        )
        assert len(new_task_list) == 0
        # Navigate to the all_tasks view that also contains the completed tasks
        view_all_tasks_link = driver.find_element(By.CSS_SELECTOR, "a.nav-all-tasks")
        view_all_tasks_link.click()
        sleep(3)
        assert driver.current_url.endswith(ALL_TASKS_URL)
        # Now check that the task is there and that it is completed
        the_task_match_list = driver.find_elements(
            By.XPATH, f"""//*[contains(text(),'{text_to_write}')]"""
        )
        assert len(the_task_match_list) == 1
        the_task = the_task_match_list[0]
        assert "task-completed" in the_task.get_attribute("class")
    finally:
        driver.quit()
