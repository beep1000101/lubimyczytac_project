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

def show_random_forest():
    st.header("Random Forest")

    st.markdown("""
    Model **Random Forest** charakteryzował się dużą dokładnością, jednak wymagał znacznie więcej zasobów obliczeniowych w porównaniu do regresji logistycznej. **Random Forest** jest algorytmem opartym na zbiorze wielu drzew decyzyjnych, które łączą się w celu uzyskania bardziej precyzyjnej klasyfikacji.

    - **Strojenie hiperparametrów**: Za pomocą **RandomizedSearchCV** zoptymalizowano parametry modelu, co pozwoliło uzyskać najlepszą jakość klasyfikacji przy użyciu miary **f1**.
    - **Selekcja hiperparametrów**: Strojenie obejmowało takie parametry jak liczba drzew w lesie (**n_estimators**), minimalna liczba próbek do podziału (**min_samples_split**), minimalna liczba próbek w liściu (**min_samples_leaf**) oraz maksymalna głębokość drzew (**max_depth**).
    
    ## Pipeline dla Random Forest
    Pipeline dla **Random Forest** wyglądał następująco:

    ```python
    ...
    # X columns for random forest: Index(['author_average_rating', 'author_number_of_people_read',
    #    'author_number_of_people_wants_to_read', 'author_number_of_fans',
    #    'author_number_of_books_written', 'author_number_of_awards',
    #    'number_of_pages', 'category', 'part_of_cycle', 'language', 'format',
    #    'description_length'],
    #   dtype='object')
    # y columns for random forrest: bestseller
    
    X_train_forest, X_test_forest, y_train_forest, y_test_forest = train_test_split(X_forest, y_forest, test_size=0.3, random_state=80085666)            
    
    # Definicja parametryzacji dla Random Forest
    random_forrest_param_grid = {
        "classifier__n_estimators": np.arange(150, 500, 20),
        "classifier__min_samples_split": np.arange(1, 30, 2),
        "classifier__min_samples_leaf": np.arange(1, 20, 1),
        "classifier__max_depth": np.arange(1, 50, 1)
    }

    # Pipeline dla Random Forest
    random_forrest_pipeline = Pipeline([
        ('classifier',
         RandomForestClassifier(class_weight='balanced',
         random_state=np.random.seed(911))),
    ])

    # Strojenie hiperparametrów przy użyciu RandomizedSearchCV
    random_forrest_grid = RandomizedSearchCV(
        random_forrest_pipeline,
        random_forrest_param_grid,
        cv=5,
        scoring="f1",
        n_jobs=-1,
        verbose=2
    )

    # Trenowanie modelu
    random_forrest_grid.fit(X_train_forest, y_train_forest)
    
    # Best parameters for random forest classifier:
    # {'classifier__n_estimators': np.int64(470),
    # 'classifier__min_samples_split': np.int64(5),
    # 'classifier__min_samples_leaf': np.int64(7),
    # 'classifier__max_depth': np.int64(33)}
    ...
    ```

    W tym przypadku:
    - **Selekcja parametrów**: Zoptymalizowano kluczowe parametry, takie jak liczba drzew, głębokość drzew, minimalna liczba próbek do podziału, minimalna liczba próbek w liściu.
    - **RandomizedSearchCV**: Użyto **RandomizedSearchCV** do wyszukiwania najlepszych hiperparametrów dla modelu **Random Forest**.
    """)


def show_knn():
    st.header("K-Nearest Neighbors (KNN)")

    st.markdown("""
    Model **K-Nearest Neighbors (KNN)** jest algorytmem klasyfikacyjnym, który działa na zasadzie przypisywania obiektów do najbliższej grupy na podstawie ich sąsiadów. Model ten charakteryzuje się prostotą implementacji i szybkością treningu, jednak może nie być odpowiedni dla bardzo dużych zbiorów danych.

    - **Strojenie hiperparametrów**: W przypadku KNN skoncentrowaliśmy się na takich parametrach jak **liczba sąsiadów (n_neighbors)**, **waga punktów (weights)**, oraz **metryka odległości (metric)**.
    - **Selekcja cech**: Podobnie jak w przypadku innych modeli, do selekcji cech użyliśmy **SelectKBest**, aby wybrać najbardziej wpływowe cechy do klasyfikacji.

    ## Pipeline dla KNN
    Pipeline dla **K-Nearest Neighbors** wyglądał następująco:

    ```python
    # Parametry do strojenia modelu KNN
    knn_param_grid = {
        'feature_selection__k': [8, 9, 10],
        'knn__weights': ['distance'],
        'knn__n_neighbors': [4, 5, 6],
        'knn__metric': ['euclidean', 'minkowski'],
        'knn__algorithm': ['auto'],
    }

    # Pipeline KNN
    knn_pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Skalowanie cech
        ('imputer', SimpleImputer(strategy='mean')),  # Uzupełnianie brakujących wartości
        ('feature_selection', SelectKBest(score_func=f_classif)),  # Selekcja cech
        ('knn', KNeighborsClassifier())  # Klasyfikator KNN
    ])

    # Strojenie hiperparametrów przy użyciu GridSearchCV
    knn_grid = GridSearchCV(
        knn_pipeline,
        knn_param_grid,
        cv=5,
        scoring="f1",  # Używamy f1 jako miary jakości modelu
        n_jobs=-1,
        verbose=2
    )

    # Trenowanie modelu KNN
    knn_grid.fit(X_train_knn, y_train_knn)
    ```

    W tym przypadku:
    - **Selekcja cech**: Zastosowano **SelectKBest** z funkcją **f_classif**, aby wybrać cechy, które najlepiej wpływają na klasyfikację.
    - **Skalowanie cech**: Wszystkie cechy zostały skalowane za pomocą **StandardScaler**, aby uzyskać lepszą wydajność modelu.
    - **Imputacja**: Użyto **SimpleImputer** do uzupełnienia brakujących wartości średnią.
    
    Oto najlepsze parametry uzyskane po strojeniach:
    
    ```python
    best_params = {
        'feature_selection__k': 9,
        'knn__weights': 'distance',
        'knn__n_neighbors': 5,
        'knn__metric': 'minkowski',
        'knn__algorithm': 'auto'
    }
    ```

    Te parametry zapewniły najlepszą jakość klasyfikacji w zadaniu, uzyskując dobrą równowagę między szybkością treningu a dokładnością klasyfikacji.
    """)


