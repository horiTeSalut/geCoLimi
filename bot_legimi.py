import os
import time
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
    
    max_retries = 20  # Liczba prób
    retry_delay = 5   # Sekundy między próbami
    
    print(f"Rozpoczynam próbę pobrania kodu (max {max_retries} podejść)...")

    for i in range(max_retries):
        try:
            driver.get("https://wbpg.org.pl")
            wait = WebDriverWait(driver, 10) # Krótszy timeout wewnątrz pętli

            # 1. Logowanie (jeśli nie jesteśmy zalogowani)
            if "Zaloguj" in driver.title or len(driver.find_elements(By.NAME, "card_number")) > 0:
                wait.until(EC.presence_of_element_located((By.NAME, "card_number"))).send_keys(CARD_NUMBER)
                driver.find_element(By.NAME, "password").send_keys(PASSWORD)
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                print(f"Podejście {i+1}: Zalogowano.")

            # 2. Szukanie przycisku pobierania
            # Jeśli przycisk jest jeszcze nieaktywny (np. przed 9:00), rzuci błędem i przejdzie do 'except'
            pobierz_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pobierz')]")))
            pobierz_btn.click()
            print("Kliknięto przycisk pobierania!")

            # 3. Odczytanie kodu
            kod_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
            kod = kod_element.text.replace("Twój kod to:", "").strip()
            
            msg = f"📚 SUKCES! Kod: {kod}"
            send_telegram_msg(msg)
            return  # Kończymy skrypt po sukcesie

        except Exception as e:
            print(f"Podejście {i+1}/{max_retries} nieudane (Serwer zajęty lub przycisk niedostępny). Czekam {retry_delay}s...")
            time.sleep(retry_delay)
            driver.refresh() # Odświeżamy stronę przed kolejną próbą

    # Jeśli pętla się skończy bez 'return'
    error_final = "❌ Nie udało się pobrać kodu po 20 próbach. Prawdopodobnie pula została wyczerpana."
    print(error_final)
    send_telegram_msg(error_final)
    driver.quit()
