import streamlit as st

def show_modeling():
    st.title("Modelowanie")

    st.markdown("""
    W tej sekcji przedstawiamy szczegóły procesu modelowania, który polegał na stworzeniu modelu klasyfikacyjnego zdolnego do identyfikacji "niedocenionych" książek z portalu **lubimyczytac.pl**. Celem było wykrycie książek, które mają potencjał komercyjny, ale nie zostały jeszcze szeroko rozpoznane.
    """)

    # Wywołanie funkcji dla poszczególnych modeli
    show_logistic_regression()
    show_random_forest()
    show_knn()

# Funkcja dla regresji logistycznej
def show_logistic_regression():
    st.header("Regresja Logistyczna")

    st.markdown("""
    Do klasyfikacji wybrano **regresję logistyczną**, jako model, który najlepiej maksymalizował **Recall**. Taki wybór był kluczowy, ponieważ zależało mi na wykrywaniu jak największej liczby bestsellerów. Regresja logistyczna okazała się wyjątkowo skuteczna w tym przypadku.

    - **Strojenie hiperparametrów**: Za pomocą **RandomizedSearchCV** zoptymalizowałem parametry modelu, co pozwoliło uzyskać wysoką jakość klasyfikacji.
    - **Selekcja cech**: Skupiliśmy się na cechach, które miały największy wpływ na predykcję bestsellerów, takich jak oceny użytkowników, liczba opinii czy dane dotyczące autorów.
    
    ## Pipeline dla regresji logistycznej
    Pipeline dla regresji logistycznej wyglądał następująco:

    ```python
    ...
    # X columns: Index(['author_average_rating', 'author_number_of_people_read',
    #    'author_number_of_people_wants_to_read', 'author_number_of_fans',
    #    'author_number_of_books_written', 'author_number_of_awards',
    #    'number_of_pages', 'category', 'part_of_cycle', 'language', 'format',
    #    'description_length', 'mean_rating', 'std_rating', 'skewness',
    #    'kurtosis'],
    #   dtype='object')
    # y columns: bestseller
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=80085666)
                
    
    number_of_features = X_train.shape[1]
    param_dist = [
        {"classifier__C": loguniform(1e-4, 10), 
        "classifier__penalty": ["l1"], 
        "classifier__solver": ["liblinear"], 
        "feature_selection__k": np.arange(1, number_of_features + 1)},
    ]

    log_reg_pipeline = Pipeline([
        ('feature_selection', SelectKBest(score_func=mutual_info_classif)),
        ('classifier', LogisticRegression(max_iter=10000, class_weight='balanced')),
    ])

    randomized_log_reg = RandomizedSearchCV(
        log_reg_pipeline, 
        param_distributions=param_dist,
        random_state=2137,
        scoring='recall', 
        n_iter=10,
        cv=5,
        verbose=1, 
        n_jobs=-1
    )

    randomized_log_reg.fit(X_train, y_train)
    
    # Best parameters for logistic regression classifier:
    # {'classifier__C': np.float64(4.036589405322333),
    # 'classifier__penalty': 'l1',
    # 'classifier__solver': 'liblinear',
    # 'feature_selection__k': np.int64(16)}
    # Best score for logistic regression classifier:
    # ['author_average_rating',
    # 'author_number_of_people_read',
    # 'author_number_of_people_wants_to_read',
    # 'author_number_of_fans',
    # 'author_number_of_books_written',
    # 'author_number_of_awards',
    # 'number_of_pages',
    # 'category',
    # 'part_of_cycle',
    # 'language',
    # 'format',
    # 'description_length',
    # 'mean_rating',
    # 'std_rating',
    # 'skewness',
    # 'kurtosis']
    ...
    ```
    - **Selekcja cech**: Zastosowano **SelectKBest** z funkcją **mutual_info_classif** do selekcji najlepszych cech, które miały największy wpływ na klasyfikację.
    - **Regresja logistyczna**: Model klasyfikacyjny z **LogisticRegression**, który był strożony pod kątem najlepszych parametrów.

    """)

# Funkcja dla modelu Random Forest
def show_random_forest():
    st.header("Random Forest")

    st.markdown("""
    Model **Random Forest** charakteryzował się dużą dokładnością, jednak wymagał znacznie więcej zasobów obliczeniowych. Strojenie hiperparametrów obejmowało:
    - **Liczba drzew (n_estimators)**,
    - **Głębokość drzew (max_depth)**,
    - **Minimalna liczba próbek w węzłach (min_samples_split, min_samples_leaf)**.
    """)

# Funkcja dla modelu KNN
def show_knn():
    st.header("K-Nearest Neighbors (KNN)")

    st.markdown("""
    Model **K-Nearest Neighbors (KNN)** był szybszy w treningu niż Random Forest i osiągnął podobne wyniki. Jednakże, z racji swojej prostoty, jego wyniki były nieco gorsze niż regresji logistycznej, mimo dużych możliwości strojenia, takich jak:
    - **Wartości k (liczba sąsiadów)**,
    - **Metryki odległości i wagi**.
    """)

