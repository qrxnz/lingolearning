## Opis projektu
Aplikacja tłumacząca zbudowana przy użyciu Flask. Pozwala użytkownikom na tłumaczenie tekstu pomiędzy różnymi językami oraz zapisywanie przetłumaczonych fraz w osobistym słowniku.

## Technologie
- Flask
- Requests
- Langdetect
- HTML/CSS
- Bootstrap (opcjonalnie, do stylizacji)

## Funkcjonalności
- Wykrywanie języka źródłowego
- Tłumaczenie tekstu na wybrany język docelowy
- Zapisywanie przetłumaczonych fraz
- Wyświetlanie zapisanych fraz w słowniku

## Instalacja
1. Sklonuj repozytorium
2. Przejdź do katalogu projektu
3. Utwórz wirtualne środowisko: `python -m venv myenv`
4. Aktywuj wirtualne środowisko:
   - Windows: `myenv\Scripts\activate`
   - macOS/Linux: `source myenv/bin/activate`
5. Zainstaluj zależności: `pip install -r requirements.txt`
6. Uruchom aplikację: `flask run`
7. Otwórz przeglądarkę i przejdź do `http://localhost:5000`

## Konfiguracja
Aby skonfigurować aplikację, utwórz plik `.env` w głównym katalogu projektu i dodaj swój klucz API:

X_RAPIDAPI_KEY=your_api_key_here

## Wymagania
- Python 3.6 lub nowszy
- Konto na [RapidAPI](https://rapidapi.com/) i klucz API: Text Translator(https://rapidapi.com/dickyagustin/api/text-translator2)

## Autor
- Maciej K
