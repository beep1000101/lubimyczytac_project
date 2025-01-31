import streamlit as st

from utils.paths import PICS_PATH
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def show_model_results():
    st.title("Ocena Modeli - Macierze Omylek")

    st.markdown("""
    W tej sekcji przedstawiamy wyniki dla trzech testowanych modeli klasyfikacyjnych: **Regresja Logistyczna**, **Random Forest** oraz **K-Nearest Neighbors (KNN)**. Celem było zoptymalizowanie modeli pod kątem wykrywania książek, które mają potencjał komercyjny, ale nie zostały jeszcze szeroko rozpoznane.

    Poniżej przedstawiamy **macierze omyłek** dla każdego z modeli, które pokazują liczbę poprawnych i błędnych klasyfikacji dla klas: **0** (brak bestselleru) oraz **1** (bestseller).
    """)

    ### Regresja Logistyczna
    st.header("Regresja Logistyczna")

    # Macierz omyłek dla regresji logistycznej
    st.image(PICS_PATH / "logistic_confusion.png", caption="Macierz omyłek - Regresja Logistyczna")

    st.markdown("""
    Model **Regresji Logistycznej** uzyskał następujące wyniki:

    - **True Negative (TN)**: 3933
    - **False Positive (FP)**: 475
    - **False Negative (FN)**: 22
    - **True Positive (TP)**: 125

    Z powyższego wynika, że model **Regresji Logistycznej** okazał się najlepszy, ponieważ najlepiej maksymalizował **Recall**, co było kluczowe w wykrywaniu książek z potencjałem komercyjnym. Choć model dobrze klasyfikuje książki o niskim potencjale (wysoka liczba **True Negatives**), wykazuje pewne trudności w wykrywaniu bestsellerów (co objawia się błędami w postaci **False Positives** i **False Negatives**). Niemniej jednak, regresja logistyczna pozostaje solidnym wyborem, szczególnie gdy zależy nam na wykrywaniu książek z potencjałem przy minimalnym ryzyku błędów klasyfikacji książek o niskim potencjale.
    """)    
            
    ### Random Forest
    st.header("Random Forest")

    # Macierz omyłek dla Random Forest
    st.image(PICS_PATH / 'random_forrest_confusion.png', caption="Macierz omyłek - Random Forest")

    st.markdown("""
    Model **Random Forest** uzyskał następujące wyniki:

    - **True Negative (TN)**: 4189
    - **False Positive (FP)**: 219
    - **False Negative (FN)**: 39
    - **True Positive (TP)**: 108

    Random Forest charakteryzował się większą dokładnością w klasyfikowaniu książek, ale nadal pojawiały się błędy klasyfikacji bestsellerów, szczególnie w przypadku **False Positives (FP)**. Z jednej strony **Random Forest** wykazywał lepszą skuteczność niż regresja logistyczna, ale z drugiej strony wymagał znacznie więcej zasobów obliczeniowych. Choć miał większą liczbę poprawnych klasyfikacji książek o niskim potencjale (**TN**), to wykazał również wyższe **FP**, co może sugerować, że częściej klasyfikuje książki jako bestsellerowe, podczas gdy w rzeczywistości nimi nie są.
    """)
    ### K-Nearest Neighbors (KNN)
    st.header("K-Nearest Neighbors (KNN)")

    # Macierz omyłek dla KNN
    st.image(PICS_PATH / "knn_confusion.png", caption="Macierz omyłek - KNN")

    st.markdown("""
    Model **K-Nearest Neighbors (KNN)** dał następujące wyniki:

    - **True Negative (TN)**: 4399
    - **False Positive (FP)**: 19
    - **False Negative (FN)**: 36
    - **True Positive (TP)**: 101

    Model **KNN** wykazał się doskonałą dokładnością w klasyfikowaniu książek o niskim potencjale komercyjnym (**TN**), ale jego skuteczność w wykrywaniu bestsellerów (wyższe **FN**) nie była idealna. Zaskakująco niskie **FP** w przypadku KNN sugerują, że model rzadko klasyfikuje książki jako bestsellerowe, ale gdy już to robi, zdarza mu się pomylić książki z potencjałem komercyjnym. Model ten jest bardzo szybki w trenowaniu, ale w zadaniach, w których precyzja klasyfikacji bestsellerów jest kluczowa, nie osiągnął takich wyników jak regresja logistyczna.

    ### Podsumowanie wyników:
    Modele wykazały różne mocne strony i wady w kontekście zadania wykrywania książek niedocenionych, które mają potencjał komercyjny, ale nie zostały szerzej rozpoznane. Regresja Logistyczna okazała się najlepsza, szczególnie jeśli zależy nam na równowadze między True Negatives a False Negatives. Model ten skutecznie wykrywał książki, które mogą być bestsellerami, minimalizując jednocześnie błędy w klasyfikacji książek, które nie mają potencjału komercyjnego.

    Random Forest poprawił ogólną jakość klasyfikacji, ale wymagał większych zasobów obliczeniowych i generował więcej False Positives, co może sugerować, że model częściej błędnie klasyfikuje książki jako niedocenione, mimo że nie mają one tego potencjału.

    KNN charakteryzował się szybszym treningiem, ale miał problemy z precyzyjnym wykrywaniem książek niedocenionych. Chociaż skutecznie klasyfikował książki o niskim potencjale komercyjnym, to jego skuteczność w wykrywaniu książek niedocenionych była niższa, co może oznaczać, że model wymaga dalszych usprawnień w celu lepszego radzenia sobie z tym zadaniem.

    Wnioskując, Regresja Logistyczna okazała się najlepszym modelem w tym eksperymencie, szczególnie gdy celem było wykrywanie książek z potencjałem komercyjnym, które zostały niedocenione lub pominięte. Model ten charakteryzował się dobrą precyzją i równowagą między klasyfikacjami, co czyniło go odpowiednim wyborem w zadaniu wykrywania książek niedocenionych z potencjałem na sukces rynkowy.    
    """)

