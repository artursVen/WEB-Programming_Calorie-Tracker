# PYTHON KALORIJU SKAITĪTĀJS
Laboratorijas darbs Nr. 2 priekšmetā WEB Programmēšana
(WEB Application Development Tools)

Django WEB lietotne, kas ļauj lietotājam uzskaitīt apēstos produktus
un aprēķināt dienas laikā uzņemtās kalorijas.

# Tehnoloģijas
- Python
- Django 5.2.17
- PostgreSQL 18.6
- psycopg 3.3.6
- HTML, CSS, JavaScript

# Funkcionalitāte
- Lietotāja pierakstīšanās un izrakstīšanās
- Pārtikas ierakstu pievienošana
- Pārtikas ierakstu labošana
- Pārtikas ierakstu dzēšana
- Tekošās dienas ierakstu saraksts un kopējo uzņemto kaloriju aprēķins
- Dinamisks kaloriju priekšskatījums ievades laikā
- Datu validācija pārlūkā un serverī

# Kaloriju aprēķins
Kopējās kalorijas = daudzums gramos * kalorijas uz 100g / 100

## Automātiskās pārbaudes
Projekta pārbaudei izmantots GitHub Actions.
Pārbaudes tiek palaistas pēc katra push un pull request.

Tiek veiktas šādas pārbaudes:
- Python koda analīze ar Ruff.
- Python koda formatējuma pārbaude ar Ruff.
- Django konfigurācijas pārbaude.
- Django testi ar atsevišķu PostgreSQL 18 datubāzi.

### Pārbaužu palaišana lokāli
Instalē arī izstrādes atkarības:

```powershell
python -m pip install -r requirements-dev.txt
```

Palaiž pārbaudes:

```powershell
python -m ruff check .
python -m ruff format --check .
python manage.py check
python manage.py test calories --keepdb
```

Komandas jāpalaiž projekta mapē ar aktivizētu virtuālo vidi.
Django testiem nepieciešama atsevišķa PostgreSQL testa datubāze.
Ja tā nav sagatavota, datubāzes lietotājam nepieciešamas tiesības to izveidot.

## Projekta uzstādīšana Windows vidē
Nepieciešams Python 3.14, PostgreSQL 18 un Git.

### 1. Lejupielādē projektu

```powershell
git clone https://github.com/artursVen/WEB-Programming_Calorie-Tracker.git
cd WEB-Programming_Calorie-Tracker
```

### 2. Izveido un aktivizē virtuālo vidi

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Virtuālā vide izolē projekta Python pakotnes no pārējiem projektiem.

### 3. Instalē atkarības

```powershell
python -m pip install -r requirements-dev.txt
```

Šī komanda instalē gan lietotnes atkarības, gan Ruff pārbaudes rīku.

### 4. Sagatavo vides mainīgos

```powershell
Copy-Item .env.example .env
```

Atver `.env` un aizpildi PostgreSQL savienojuma iestatījumus.
Norādītajai datubāzei un lietotājam jābūt iepriekš izveidotiem
PostgreSQL serverī.

`SECRET_KEY` vērtībai izveido jaunu Django atslēgu:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Iegūto vērtību ievieto `.env` mainīgajā `SECRET_KEY`.
Lokālai izstrādei izmanto `DEBUG=True`.

Failā `.env` glabājas paroles un atslēgas. Tas netiek pievienots Git.

### 5. Izveido datubāzes tabulas

Kad PostgreSQL datubāze un `.env` iestatījumi ir sagatavoti, palaid:

```powershell
python manage.py migrate
```

Migrācijas izveido Django un kaloriju uzskaites tabulas datubāzē.

### 6. Izveido lietotāju

```powershell
python manage.py createsuperuser
```

Izpildi termināļa norādes, ievadot lietotājvārdu, e-pastu un paroli.
Paroles ievades laikā simboli terminālī netiek attēloti.

Izveidoto kontu var izmantot gan lietotnē, gan administratora panelī.
Laboratorijas darba versijā publiska lietotāju reģistrācija nav pieejama.

### 7. Palaid izstrādes serveri

```powershell
python manage.py runserver
```

Atver pārlūkā:

- Lietotne: http://127.0.0.1:8000/
- Administratora panelis: http://127.0.0.1:8000/admin/

Piesakies ar iepriekš izveidoto lietotāju.

Serveri aptur ar `Ctrl+C`.
Django izstrādes serveris paredzēts lokālai izstrādei.