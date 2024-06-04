# Automatyzacja Oceny Sprawozdań Studenckich przy Użyciu Dużych Modeli Językowych (StudentReportLLMs)

**Autorzy:** Jakub Pawlak, Magdalena Pakuła, Piotr Hynasiński, Artur Pietrzak, Rafał Górniak

## Cel Projektu

Celem projektu jest stworzenie systemu wykorzystującego zaawansowane modele językowe do automatycznej oceny sprawozdań studenckich. System ma na celu analizę jakości treści oraz ocenę zgodności z wytycznymi projektowymi, zapewniając obiektywne i precyzyjne narzędzie wspomagające proces edukacyjny.

## Opis Systemu

W ramach projektu konieczne jest zaprojektowanie i implementacja systemu wykorzystującego duże modele językowe do oceny sprawozdań studenckich. Ocena będzie dotyczyć dwóch kluczowych aspektów:

1. **Jakość treści** - Analiza jakości treści przy użyciu modeli językowych takich jak BERT czy T5.
2. **Zgodność z wytycznymi projektowymi** - Ewaluacja zgodności z wytycznymi przy użyciu modeli jak LLaMA-2 lub Mistral.

Projekt obejmuje również:
- Odczyt i analizę plików w formatach PDF, Word, LaTeX.
- Definiowanie specyficznych kryteriów oceny przez użytkownika.
- Ocenę oryginalności tekstu w celu zapobiegania plagiatom.
- Stworzenie intuicyjnego interfejsu użytkownika do formułowania zapytań dotyczących kryteriów oceny.

Efektywność, precyzja oraz użyteczność systemu będą kluczowymi kryteriami oceny projektu. Dokumentacja projektowa będzie szczegółowo opisywać architekturę systemu, wykorzystane technologie, proces implementacji oraz wyniki przeprowadzonych testów.

## Zakres Prac

### Analiza i Projektowanie

- Zdefiniowanie głównych funkcji systemu, w tym oceny jakości treści, zgodności z wytycznymi projektowymi oraz oceny oryginalności prac.
- Określenie wymagań technicznych, w tym integracji z formatami plików PDF, Word, LaTeX.

### Wybór Technologii

- Dobór odpowiednich modeli językowych dla oceny jakości treści (przykładowo BERT, T5) oraz dla ewaluacji zgodności z wytycznymi projektu (np. Mistral).
- Wybór bazy danych i technologii do zarządzania wektorami dla realizacji zadania Information Retrieval.

### Implementacja

- Rozwój interfejsu użytkownika umożliwiającego łatwą interakcję z systemem oraz formułowanie zapytań tekstowych.
- Integracja wybranych modeli językowych z systemem bez potrzeby ich dodatkowego szkolenia.
- Implementacja funkcji odczytu i przetwarzania plików PDF oraz Word.

### Testowanie i Ewaluacja

- Przeprowadzenie testów systemu przy użyciu danych testowych generowanych przez modele językowe takie jak GPT-3.5 lub GPT-4.
- Ocena skuteczności systemu w kontekście celów projektowych.

### Dokumentacja

- Przygotowanie szczegółowej dokumentacji projektowej, w tym opisu architektury systemu, wykorzystanych technologii, oraz wyników testów i ewaluacji.

## Technologie
- Języki programowania: Python
- Frameworki i biblioteki: PyQt5, BERT, T5, LLaMA-2, Mistral
- Bazy danych: MongoDB, Qdrant
- Narzędzia do zarządzania plikami: PyMuPDF (PDF), python-docx (Word)

