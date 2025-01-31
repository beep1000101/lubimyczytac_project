# lubimyczytac_project

Projekt mający na celu stworzenie modelu klasyfikacyjnego, który wykrywa "niedocenione" książki na podstawie danych z portalu **lubimyczytac.pl**. Modele wykorzystywane w tym projekcie to m.in. regresja logistyczna, Random Forest i K-Nearest Neighbors (KNN), które pomagają w identyfikacji książek o potencjale komercyjnym.

## Opis

To eksperyment **data science end-to-end**, który obejmuje cały proces od pozyskiwania danych, przez czyszczenie, modelowanie, aż po budowę dashboardu w **Streamlit**. W projekcie wykorzystano własne podejście do **sourcingu danych**, modelowania predykcyjnego i implementacji interfejsu użytkownika.

## Instrukcja uruchomienia

1. **Utworzenie wirtualnego środowiska**:
   - Zainstaluj Python w wersji 3.13.
   - Stwórz wirtualne środowisko:
     ```bash
     python3.13 -m venv venv
     ```

2. **Instalacja wymaganych bibliotek**:
   - Zainstaluj wymagane biblioteki za pomocą `pip`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Uruchomienie aplikacji**:
   - Po zainstalowaniu wymaganych pakietów uruchom aplikację:
     ```bash
     streamlit run app.py
     ```

4. **Przygotowanie danych i modeli**:
   - Upewnij się, że odpowiednie pliki z danymi i modelami `.pkl` są dostępne w odpowiednich folderach, zgodnie z instrukcjami w kodzie.

## Środowisko

Projekt testowany na **Fedora 41** z Python 3.13.

Projekt używa bibliotek takich jak `joblib`, `pandas`, `scikit-learn` i `streamlit`.
