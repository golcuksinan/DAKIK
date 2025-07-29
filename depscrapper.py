import os
import django
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Django ortamını hazırla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.academic.models import Faculty, University, Department

def main():
    firefox_options = Options()
    firefox_options.headless = False  # istersen başsız modda çalıştır
    firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0")
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference("useAutomationExtension", False)

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    with open('values.txt', 'r') as file:
        values = file.readlines()

    deps_seen = set()  # Set to track seen departments
    with open('depnames.txt', 'w', encoding='utf-8') as file:
        for university_code in values:
            university_code = university_code.strip()
            driver.get("https://yokatlas.yok.gov.tr/lisans-anasayfa.php")

            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'flip1'))).click()
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button'))).click()
            print(f"İşlem yapılıyor: {university_code}")

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

                uni_name_raw = driver.find_element(By.XPATH, "//div[@class='page-header']/h3").text
                uni_name = uni_name_raw.split("ÜNİVERSİTESİ")[0].strip() + " ÜNİVERSİTESİ"

                uni = University.objects.filter(name=uni_name).first()
                if not uni:
                    print(f"UYARI: Üniversite bulunamadı: {uni_name}")
                    continue

                faculty_containers = driver.find_elements(By.XPATH, '//*[@id="bs-collapse"]/div')
                faculty_containers2 = driver.find_elements(By.XPATH, '//*[@id="bs-collapse2"]/div')
                faculty_containers.extend(faculty_containers2)

                for container in faculty_containers:
                    try:
                        faculty_element = container.find_element(By.XPATH, './div/h4/a/small/font')
                        faculty_name_text = faculty_element.text.replace('(', '').replace(')', '').strip()

                        faculty, created = Faculty.objects.get_or_create(
                            name=faculty_name_text,
                            university=uni
                        )
                        if created:
                            print(f"Yeni fakülte eklendi: {faculty_name_text}")

                        department_elements = container.find_elements(By.XPATH, './div/h4/a/div')
                        for dept_element in department_elements:
                            department_name_text = dept_element.text.strip()
                            if department_name_text:
                                department, dept_created = Department.objects.get_or_create(
                                    name=department_name_text,
                                    faculty=faculty
                                )
                                if dept_created:
                                    print(f"  Yeni bölüm eklendi: {department_name_text}")
                                if department_name_text not in deps_seen:
                                    file.write(f'{department_name_text} - {faculty_name_text} - {uni_name}\n')
                                    deps_seen.add(department_name_text)
                    except Exception as e:
                        print(f'Fakülte/bölüm işleme hatası: {e}')

                print('-' * 50)
            except Exception as e:
                print(f'{university_code} üniversitesi için fakülte bilgileri alınamadı. Hata: {e}')

    driver.quit()

if __name__ == "__main__":
    main()
