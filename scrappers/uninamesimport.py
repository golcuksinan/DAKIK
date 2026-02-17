import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dtp import app, db  # Assuming create_app is your function to initialize the Flask app
from dtp.models import University

# Tarayıcıyı başlatan fonksiyon
def start_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://yokatlas.yok.gov.tr/lisans-anasayfa.php')
    return driver

# Sayfada beklenen elementin yüklenmesini bekleme
def wait_for_element(driver, by, value):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

# Veritabanına üniversite ekleme
def add_university_to_db(university_name):
    university = University(name=university_name)
    db.session.add(university)
    db.session.commit()

def main():
    # Flask uygulaması başlatma
      # Bu fonksiyon Flask uygulamanızı oluşturuyor olmalı
    with app.app_context():  # Uygulama bağlamını sağlama
        # Tarayıcıyı başlat
        driver = start_driver()
        time.sleep(1)

        # Butona tıklama işlemi
        wait_for_element(driver, By.ID, 'flip1')
        driver.find_element(By.ID, 'flip1').click()

        # İkinci butona tıklama işlemi
        wait_for_element(driver, By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button')
        driver.find_element(By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button').click()

        # Listeyi al
        li_tags = driver.find_elements(By.XPATH, '//select//option')

        print('Lisans Programları:')
        for li in li_tags:
            # Boş veya istenmeyen elemanları filtreleme
            if li.text in ['Seç...', '']:
                continue
            if li.text == 'ABAZA DİLİ VE EDEBİYATI':
                break
            # Üniversite ismini yazdır ve veritabanına ekle
            print(li.text)
            add_university_to_db(li.text)

        # Tarayıcıyı kapat
        driver.quit()

if __name__ == '__main__':
    main()
