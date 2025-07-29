import os
import django
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup Django environment ---

# Set this to your Django project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

# Now import models
from apps.academic.models import Faculty, University


def main():
    firefox_options = Options()
    firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0")
    # Optional: run headless
    # firefox_options.headless = True

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    with open('values.txt', 'r') as file:
        values = file.readlines()

    with open('facnames.txt', 'w', encoding='utf-8') as file:
        for university_code in values:
            university_code = university_code.strip()
            driver.get("https://yokatlas.yok.gov.tr/lisans-anasayfa.php")
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'flip1'))).click()
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button'))).click()
            print(f"Processing: {university_code}")

            select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "univ")))

            select = Select(select_element)
            try:
                driver.execute_script("""
                    var select = arguments[0];
                    var value = arguments[1];
                    select.value = value;
                    select.dispatchEvent(new Event('change'));
                """, select_element, str(university_code))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bs-collapse"]/div/div/h4/a/small/font')))
                
                faculty_names = driver.find_elements(By.XPATH, '//*[@id="bs-collapse"]/div/div/h4/a/small/font')
                faculty_names2 = driver.find_elements(By.XPATH, '//*[@id="bs-collapse2"]/div/div/h4/a/small/font')
                faculty_names.extend(faculty_names2)

                uni_name_raw = driver.find_element(By.XPATH, "//div[@class='page-header']/h3").text
                uni_name = uni_name_raw.split("ÜNİVERSİTESİ")[0].strip() + " ÜNİVERSİTESİ"

                uni = University.objects.filter(name=uni_name).first()
                if not uni:
                    print(f"WARNING: University not found: {uni_name}")
                    continue

                print(f'{uni_name} Faculties:')
                for faculty_name in faculty_names:
                    faculty_name_to_db = faculty_name.text.replace('(', '').replace(')', '').strip()
                    print(f'  - {faculty_name_to_db}')
                    faculty, created = Faculty.objects.get_or_create(
                        name=faculty_name_to_db,
                        university=uni
                    )
                    file.write(f'{faculty_name_to_db} - {uni_name}'+ '\n')
                    if created:
                        print(f"Added: {faculty_name_to_db}")
                    else:
                        print(f"Exists: {faculty_name_to_db}")

                print('-' * 50)
            except Exception as e:
                print(f"Failed to fetch faculties for {university_code}: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
