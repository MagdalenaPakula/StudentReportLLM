# Automatyzacja Oceny Sprawozdań Studenckich przy Użyciu Dużych Modeli Językowych (StudentReportLLMs)

**Autorzy:** Jakub Pawlak, Magdalena Pakuła, Piotr Hynasiński, Artur Pietrzak, Rafał Górniak

## 🎯 Cel Projektu

Celem projektu jest stworzenie systemu wykorzystującego zaawansowane modele językowe do automatycznej oceny sprawozdań studenckich, wspomagającego proces edukacyjny. System analizuje jakość treści oraz ocenia zgodność z wytycznymi projektowymi, zapewniając obiektywne i precyzyjne narzędzie dla uczelni oraz studentów.

## 📖 Opis Systemu

System automatycznej oceny sprawozdań studenckich opiera się na dużych modelach językowych i obejmuje:

1. **Analizę jakości treści** – Wykorzystuje modele takie jak BERT i T5 do oceny merytorycznej i językowej raportów.
2. **Sprawdzanie zgodności z wytycznymi projektowymi** – Używa modeli LLaMA-2 oraz Mistral, by zapewnić zgodność sprawozdań z założonymi kryteriami.

Dodatkowe funkcje systemu:
- Obsługa plików w formatach PDF, Word, LaTeX.
- Umożliwienie definiowania kryteriów oceny przez użytkownika.
- Sprawdzanie oryginalności tekstu i wykrywanie plagiatów.
- Stworzenie intuicyjnego interfejsu użytkownika do zarządzania kryteriami oceny i wynikami analizy.

Efektywność, precyzja oraz użyteczność systemu będą kluczowymi kryteriami sukcesu projektu.

## 📝 Zakres Prac

### Analiza i Projektowanie

- **Zdefiniowanie głównych funkcji**: ocena jakości treści, zgodności z wytycznymi, oraz oryginalności prac.
- **Określenie wymagań technicznych**: obsługa różnych formatów plików (PDF, Word, LaTeX) i integracja odpowiednich modeli językowych.

### Wybór Technologii

- **Modele językowe**: dobór modeli takich jak BERT, T5 do oceny jakości treści oraz modeli jak LLaMA-2 i Mistral do sprawdzania zgodności z wytycznymi.
- **Bazy danych i technologie wektorowe**: wybór MongoDB oraz Qdrant do zarządzania danymi i wyszukiwania informacji.

### Implementacja

- **Interfejs użytkownika**: projektowanie intuicyjnego UI umożliwiającego łatwą interakcję i formułowanie kryteriów oceny.
- **Integracja modeli językowych**: włączenie wybranych modeli bez potrzeby dodatkowego szkolenia.
- **Obsługa plików**: implementacja odczytu i analizy plików PDF oraz Word przy użyciu PyMuPDF i python-docx.

### Testowanie i Ewaluacja

- **Testowanie z użyciem danych syntetycznych**: testy na danych generowanych przez modele GPT-3.5 i GPT-4.
- **Ocena skuteczności**: ewaluacja systemu na podstawie zdefiniowanych celów projektowych.

### Dokumentacja

- **Przygotowanie dokumentacji**: szczegółowy opis architektury systemu, zastosowanych technologii oraz wyników testów i ewaluacji.

## 💻 Technologie

- **Języki programowania**: Python 3.12.2
- **Frameworki i biblioteki**: PyQt5, BERT, T5, LLaMA-2, Mistral
- **Bazy danych**: MongoDB, Qdrant
- **Narzędzia do zarządzania plikami**: PyMuPDF (PDF), python-docx (Word)
