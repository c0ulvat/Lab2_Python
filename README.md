Log Analizatoru

Bu Python skripti, server loglarını analiz etmək, uğursuz giriş cəhdlərini müəyyən etmək, qara siyahıya alınmış domenlər haqqında məlumat toplamaq və nəticələri müxtəlif formatlarda saxlamaq üçün nəzərdə tutulmuşdur.

İşləmə Prinsipi

Skript aşağıdakı addımları yerinə yetirir:
	1.	Logların Pars Edilməsi:
access_log.txt faylından log qeydlərini oxuyur və müvafiq məlumatları (IP ünvanı, tarix, HTTP metodu, URL və status kodu) çıxarır.
	2.	URL-lərin Analizi:
Bütün URL-ləri və onların status kodlarını analiz edir, nəticələri url_status_report.txt faylında saxlayır.
	3.	Uğursuz Girişlərin Siyahıya Alınması:
40x status kodları ilə nəticələnmiş URL-ləri analiz edir və məlumatları malware_candidates.csv faylında saxlayır.
	4.	Təhdid Məlumatlarının Əldə Edilməsi:
Müəyyən edilmiş URL-dən (http://127.0.0.1:8000/threat_feed.html) qara siyahıya alınmış domenlər haqqında məlumatı “Selenium” kitabxanası vasitəsilə web scraping edir.
	5.	Uyğunlaşdırma:
Parse edilmiş loglardakı URL-ləri əldə edilmiş qara siyahıya alınmış domenlərlə uyğunlaşdırır və nəticələri JSON formatında (alert.json) saxlayır.
	6.	Məlumatların Ümumiləşdirilməsi:
Analiz nəticələrini qısa şəkildə ümumiləşdirərək summary_report.json faylında saxlayır.

Tələblər
	•	Python 3
	•	Aşağıdakı Python kitabxanaları:
	•	re (daxili kitabxana)
	•	json (daxili kitabxana)
	•	csv (daxili kitabxana)
	•	selenium (pip install selenium)

İstifadə
	1.	Virtual mühit yaradın:

python -m venv myenv  


	2.	Virtual mühiti aktivləşdirin:
	•	Linux/MacOS:

source myenv/bin/activate  


	•	Windows:

myenv\Scripts\activate  


	3.	Lazımlı kitabxanaları quraşdırın:

pip install -r requirements.txt  


	4.	Lokal Veb Serveri Başladın:
Təhdid məlumatlarını toplamaq üçün index.html faylını lokal HTTP serverində işlədin:

python -m http.server 8000  


	5.	Skripti işə salın:

python log_analyzer.py  

Fayl Strukturası

Bütün fayllar eyni qovluqda olmalıdır:
	•	log_analyzer.py (Bu skript)
	•	access_log.txt (Analiz ediləcək log faylı)
	•	index.html (Qara siyahıya alınmış domenlər haqqında məlumatları saxlayan HTML faylı)
	•	url_status_report.txt (URL-lər və onların status kodları)
	•	malware_candidates.csv (Uğursuz girişlər (CSV))
	•	alert.json (Uyğunlaşdırılmış təhdid məlumatları (JSON))
	•	summary_report.json (Ümumiləşdirilmiş analiz nəticələri)

  
