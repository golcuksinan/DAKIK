import os
import django
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace with your Django settings module
django.setup()

from apps.academic.models import University  # Replace with your app name

def start_driver():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.get('https://yokatlas.yok.gov.tr/lisans-anasayfa.php')
    return driver

def wait_for_element(driver, by, value):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

def add_university_to_db(name, code=None, city=None, country='Turkiye'):
    uni, created = University.objects.get_or_create(
        name=name if name else None,  # Using name as fallback for code if no code available
        defaults={
            'code': code,
            'city': city if city else '',
            'country': country,
        }
    )
    if created:
        print(f"Added: {name}")
    else:
        print(f"Already exists: {name}")

def main():
    driver = start_driver()
    time.sleep(1)

    #wait_for_element(driver, By.ID, 'flip1')
    #driver.find_element(By.ID, 'flip1').click()
    #wait_for_element(driver, By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button')
    #driver.find_element(By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button').click()

    li_tags = driver.find_elements(By.XPATH, '//select//option')
    with open('uninames.txt', 'w', encoding='utf-8') as file:
        print('Lisans Programları:')
        for li in li_tags:
            if li.text in ['Seç...', '']:
                continue
            if li.text == 'ABAZA DİLİ VE EDEBİYATI':
                break
            university_name = li.text.strip()
            file.write(university_name + '\n')
            # If you can parse code or city from li.text or another attribute, do it here
            # For now just save the name
            add_university_to_db(name=li.text)

    driver.quit()

if __name__ == '__main__':
    main()
