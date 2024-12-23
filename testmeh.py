import re
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Çıxış fayllarının yolları
LOG_FILE = "access_log.txt"
URL_STATUS_REPORT_FILE = "url_status_report.txt"
MALWARE_FILE = "malware_candidates.csv"
MATCHED_ALERTS = "alert.json"

# 1-ci addım: Girişlərdən müvafiq məlumatları çıxarmaq

def parse_logs(file_path):
    parsed_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Updated pattern remains unchanged
                match = re.search(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP/.*?" (\d+) (\d+)', line)
                if match:
                    ip, date, method, endpoint, status, _ = match.groups()
                    # Append all fields, including the endpoint (URL)
                    parsed_data.append((ip, date, method, endpoint, status))
        print(f"{len(parsed_data)} giriş qeydi parse edildi.")
        return parsed_data
    except Exception as e:
        print(f"Girişləri parse edərkən səhv: {e}")
        return []

# 2-ci addım: Bütün URL-lər və onların status kodları
def status_report(parsed_data):
    with open(URL_STATUS_REPORT_FILE, 'w') as txt_file:
        txt_file.write("Bütün URL-lər və onların status kodları:\n")
        for _,_,_,endpoint,status in parsed_data:
            txt_file.write(f"{endpoint}: {status}\n")
        print(f"Giriş analizi {URL_STATUS_REPORT_FILE} faylında saxlanıldı.")

# # 3-cü addım: 404 səhvli URL-ləri və onların saylarını sadalayın.
def write_to_csv(parsed_data):
    with open(MALWARE_FILE, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["URL", "SAY"])
        for _,_,_,endpoint,status in parsed_data:
            if status.startswith("40"):
                writer.writerow([endpoint, status])  # 404 səhvli URL-ləri və onların saylarını sadalayir
    print(f"Log məlumatları {MALWARE_FILE} faylında yazıldı.")


# 5-ci addım: Təhlükə məlumatlarını (IP ünvanları və təsvirləri) əldə etmək
def scrape_blacklisted_domains(url):
    try:
        # Firefox WebDriver qurulması
        driver = webdriver.Firefox()

        # URL açmaq və siyahıdakı domenləri əldə etmək
        driver.get(url)

        # Blacklisted Domains başlığı altındakı siyahı elementlərini tapmaq
        domains = driver.find_elements(By.XPATH, "//h2[text()='Blacklisted Domains']/following-sibling::ul/li")
        blacklisted_domains = [domain.text.strip() for domain in domains]

        driver.quit()
        if blacklisted_domains:
            return blacklisted_domains
        else:
            print("Heç bir qara siyahıya salınmış domen tapılmadı.")
            return []

    except Exception as e:
        print(f"Səhv: {e}")
        return []

# # 6-cı addım: Girişləri təhlükə məlumatları ilə uyğunlaşdırmaq
def matched_alerts_code(parsed_data, alerts_url):
    matched_alerts = {}
    for _, _, _, endpoint, status in parsed_data:
        for i in alerts_url:
            if i in endpoint:
                matched_alerts[endpoint] = {
                    "status": status,
                }
    return matched_alerts

def main():
    # Server loglarını parse etmək
    parsed_data = parse_logs(LOG_FILE)
    if not parsed_data:
        print("Log məlumatları parse edilə bilmədi. Çıxılır.")
        return

    # Uğursuz girişləri analiz etmək
    url_status = status_report(parsed_data)

    # Parse edilmiş məlumatları CSV-yə yazmaq
    write_to_csv(parsed_data)

    # Təhlükə məlumatlarını əldə etmək
    blacklist_url = "http://127.0.0.1:8000/threat_feed.html"
    alerts_url = scrape_blacklisted_domains(blacklist_url)


    # Qara siyahıya salınmış uyğun URL-ləri saxlayın
    matched_alerts = matched_alerts_code(parsed_data, alerts_url)
    with open(MATCHED_ALERTS, "w") as json_file:
        json.dump(matched_alerts, json_file, indent=4)
        print(f"Uyğun gələn təhdid IP-ləri {MATCHED_ALERTS} faylına yadda saxlanıldı.")


# Əgər bu skript icra edilirsə, əsas funksiyanı çalışdırırıq
if __name__ == "__main__":
    main()