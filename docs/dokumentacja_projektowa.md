# Dokumentacja Projektowa - StudentReportLLMs

## Cel projektu

Celem projektu jest stworzenie systemu wykorzystującego zaawansowane modele językowe do automatycznej oceny sprawozdań
studenckich.
System ma na celu analizę jakości treści oraz ocenę zgodności z wytycznymi projektowymi, zapewniając obiektywne i
precyzyjne narzędzie wspomagające proces edukacyjny.

## Zespół projektowy

- Magdalena Pakuła 
- Jakub Pawlak
- Piotr Hynasiński
- Artur Pietrzak
- Rafał Górniak

# Zakres pojektu

## Zakres funkcjonalny

System ma wykorzystywać duże modele językowe do oceny sprawozdań studenckich.
Ocena ma dotyczyć dwóch kluczowych aspektów: jakości treści i zgodności z wytycznymi projektowymi (konkretnego zadania,
którego dotyczy sprawozdanie)

Wymagane będzie zintegrowanie i wykorzystanie zaawansowanych modeli językowych, bez konieczności ich dodatkowego
szkolenia (fine-tuning).

Projekt powinien obejmować funkcjonalność odczytu i analizy plików w formatach PDF, Word, LaTeX. Dodatkowo, system musi
umożliwiać definiowanie przez operatora specyficznych kryteriów oceny, adaptowalnych do różnorodnych wymagań
projektowych.

Projekt zakłada również opracowanie metody oceny oryginalności tekstu, aby zapobiegać plagiatom i promować unikalność
prac studenckich.

## Zakres niefunkcnojalny

Ważnym elementem będzie stworzenie intuicyjnego interfejsu użytkownika, który pozwoli na łatwe formułowanie zapytań
dotyczących specyficznych kryteriów oceny dla ogółu dostępnych prac, takich jak często popełniane błędy czy powtarzające
się braki w sprawozdaniach.

Kluczowymi elementami będą efektywność, precyzja oraz użyteczność systemu.

Ważne będzie również stworzenie szczegółowej dokumentacji projektowej.

# Analiza wymagań
Poniżej znajdują się wszystkie wymagania funkcjonalne i niefunkcjonalne projektu
## Wymagania funkcjonalne

1. Zarządzanie kontami użytkowników
    1. Tworzenie nowych kont
    2. Modyfikacja przywilejów istniejących kont
2. Formułowaie przez nauczyciela kryteriów oceny pracy
3. Analiza jakościowa treści sprawozdania
4. Analiza zgodności z wymaganiami treści sprawozdania
5. Porównanie pod kątem plagiatu z historycznymi pracami zapisanymi w uczelnianym archiwum
6. Odczyt różnych formatów plików (.docx, .pdf, .tex)
7. Zabezpieczenie przed atakami typu *prompt injection*

## Wymagania niefunkcnojalne

1. Intuicyjność i reaktywność interfejsu użytkownika
2. Wysokie wartości miar porównujących wyniki automatycznego oraz manualnego sprawdzania:
    1. F1-score
    2. Precision
    3. Recall
    4. Accuracy
3. Pozytywna korelacja pomiędzy wynikami automatycznego i manualnego sprawdzania
4. Automatyczne testy poprawności działania systemu
5. Szczegółowa dokumentacja projektowa
6. Satysfakcjonujący czas weryfikacji pracy przez system

# Projekt systemu

## Architektura systemu

## Struktura bazy danych

Z racji na ogranicznony kontekst modelów językowych, prace na czas sprawdzania będą umieszczane w wektorowej bazie danych,
która będzie odpytywana w celu ekstrakcji semantycznie powiązanych fragmentów sprawozdań.

Długotrwałe przechowywanie prac na potrzeby sprawdzania plagiatowego, ze względu na ograniczenia wynikające z praw autorskich, 
będą musiały być przechowywane przez indywidualne uczelnie, a projektowany system będzie jedynie uzyskiwać do nich tymczasowy dostęp.

## Interfejs użytkownika
Interfejs użytkownika będzie zaprojektowany tak, aby był intuicyjny i łatwy w obsłudze. 
Użytkownicy będą mogli:
- Logować i rejestrować się do systemu
- Przesyłać prace uczniów do oceny
- Wprowadzać i modyfikować kryteria oceny
- Przeglądać wyniki ocen i analizy jakościowej

# Harmonogram

# Zarządzanie ryzykiem

# Testowanie

## Plany testów

## Scenariusze testowe

# Wdrożenie

## Struktura wdrożenia

## Plan wdrożenia 


