# geCoLimi
script goes for Code on Limi page doing no harm

Wybór Python i Selenium to najlepsza droga do automatyzacji tego procesu, ponieważ strona biblioteki wymaga zalogowania i interakcji z elementami dynamicznymi. Poniżej znajdziesz kompletny przewodnik, jak przygotować taki skrypt i zamknąć go w kontenerze Docker.
1. Logika działania skryptu
Głównym celem jest wejście na stronę legimi.wbpg.org.pl dokładnie o godzinie 09:00, 10. dnia miesiąca. Skrypt powinien: 
WOJEWÓDZKA I MIEJSKA BIBLIOTEKA PUBLICZNA w Gdańsku
WOJEWÓDZKA I MIEJSKA BIBLIOTEKA PUBLICZNA w Gdańsku
Zalogować się numerem karty i hasłem bibliotecznym.
Kliknąć przycisk „Pobierz kod”.
Zapisać wyświetlony kod (np. do pliku lub wysłać powiadomieniem). 
WOJEWÓDZKA I MIEJSKA BIBLIOTEKA PUBLICZNA w Gdańsku
WOJEWÓDZKA I MIEJSKA BIBLIOTEKA PUBLICZNA w Gdańsku
2. Przykładowy skrypt (Python + Selenium)
Do poprawnego działania w kontenerze Docker, skrypt musi używać opcji headless (bez interfejsu graficznego).

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfiguracja danych logowania (najlepiej przez zmienne środowiskowe)
CARD_NUMBER = os.getenv('CARD_NUMBER', 'TWOJ_NUMER_KARTY')
PASSWORD = os.getenv('PASSWORD', 'TWOJE_HASLO')
URL = "https://wbpg.org.pl"

def get_legimi_code():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tryb bez okna (wymagany w Dockerze)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)
        
        # 1. Logowanie
        print("Logowanie...")
        wait.until(EC.presence_of_element_located((By.NAME, "card_number"))).send_keys(CARD_NUMBER)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # 2. Oczekiwanie na przycisk pobierania (często pojawia się punkt 9:00)
        print("Szukanie przycisku pobierania kodu...")
        # Zakładając, że przycisk ma tekst 'Pobierz kod' lub konkretne ID
        pobierz_btn = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Pobierz")))
        pobierz_btn.click()

        # 3. Odczytanie kodu z ekranu
        time.sleep(2) # Chwila na przeładowanie
        kod_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "code-value"))) # Przykładowa klasa
        print(f"TWÓJ KOD TO: {kod_element.text}")
        
        # Opcjonalnie: Zapis do pliku montowanego w Dockerze
        with open("kod_legimi.txt", "w") as f:
            f.write(kod_element.text)

    except Exception as e:
        print(f"Błąd: {e}")
        driver.save_screenshot("error.png") # Zrzut ekranu w razie błędu
    finally:
        driver.quit()

if __name__ == "__main__":
    get_legimi_code()

