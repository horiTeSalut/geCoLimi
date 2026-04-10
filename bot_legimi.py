import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfiguracja z zmiennych środowiskowych
CARD_NUMBER = os.getenv('CARD_NUMBER')
PASSWORD = os.getenv('PASSWORD')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_msg(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Błąd wysyłania do Telegrama: {e}")

def get_legimi_code():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://wbpg.org.pl")
        
        # 1. Logowanie
        wait.until(EC.presence_of_element_located((By.NAME, "card_number"))).send_keys(CARD_NUMBER)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Zalogowano pomyślnie.")

        # 2. Kliknięcie w przycisk (selektor dopasowany do przycisku 'Pobierz kod')
        # Uwaga: Selektor może wymagać aktualizacji po zmianach na stronie WiMBP
        pobierz_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pobierz')]")))
        pobierz_btn.click()

        # 3. Odczytanie kodu
        # Szukamy elementu, który pojawia się po kliknięciu (np. alertu lub tekstu z kodem)
        kod_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        kod = kod_element.text.replace("Twój kod to:", "").strip()
        
        msg = f"📚 Sukces! Twój kod Legimi z WiMBP: {kod}"
        print(msg)
        send_telegram_msg(msg)

    except Exception as e:
        error_msg = f"❌ Błąd podczas pobierania kodu: {str(e)[:100]}"
        print(error_msg)
        send_telegram_msg(error_msg)
    finally:
        driver.quit()

if __name__ == "__main__":
    get_legimi_code()
