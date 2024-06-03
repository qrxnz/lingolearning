import requests
from flask import Flask, render_template, request, make_response, redirect, url_for
from dotenv import load_dotenv
import os
from langdetect import detect, LangDetectException
import secrets

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

app = Flask(__name__)

# Konfiguracja API URL i klucza
API_URL = "https://text-translator2.p.rapidapi.com/translate"
API_KEY = os.getenv("X_RAPIDAPI_KEY")

# Obsługiwane języki
SUPPORTED_LANGUAGES = ["es", "fr", "de", "en", "pl"]

# Generowanie tajnego klucza dla sesji
app.secret_key = secrets.token_urlsafe(32)

# Zmienna globalna do przechowywania słownika tłumaczeń
translation_dictionary = {}

@app.route("/", methods=["GET", "POST"])
def translator():
    if request.method == "POST":
        # Pobieranie tekstu i docelowego języka z formularza
        text = request.form["text"]
        target_lang = request.form["target_lang"]

        # Wykrywanie języka źródłowego
        try:
            source_lang = detect(text)
        except LangDetectException:
            source_lang = "pl"  # Domyślnie ustawienie na polski, jeśli wykrycie języka nie powiedzie się

        # Przygotowanie nagłówków do zapytania API
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }

        # Przygotowanie payloadu do zapytania API
        payload = f"source_language={source_lang}&target_language={target_lang}&text={text}"

        # Wysłanie zapytania POST do API
        response = requests.post(API_URL, data=payload, headers=headers)

        # Sprawdzenie odpowiedzi API
        if response.status_code == 200:
            # Pobranie przetłumaczonego tekstu z odpowiedzi
            translated_text = response.json()["data"]["translatedText"]
            # Renderowanie szablonu z przetłumaczonym tekstem
            resp = make_response(render_template("translator.html", translated_text=translated_text, source_lang=source_lang, target_lang=target_lang, supported_languages=SUPPORTED_LANGUAGES))
            # Ustawienie ciasteczka z wybranym językiem docelowym
            resp.set_cookie("target_lang", target_lang)
            return resp
        else:
            # Renderowanie szablonu z błędem, jeśli tłumaczenie się nie powiedzie
            return render_template("translator.html", error="Błąd tłumaczenia.", supported_languages=SUPPORTED_LANGUAGES)

    # Pobieranie zapisanego języka docelowego z ciasteczek
    target_lang = request.cookies.get("target_lang", SUPPORTED_LANGUAGES[0])
    return render_template("translator.html", target_lang=target_lang, supported_languages=SUPPORTED_LANGUAGES)

@app.route("/save_translation", methods=["POST"])
def save_translation():
    global translation_dictionary
    # Pobieranie oryginalnego i przetłumaczonego tekstu z formularza
    source_text = request.form["source_text"]
    translated_text = request.form["translated_text"]
    # Zapisywanie tłumaczenia do słownika
    translation_dictionary[source_text] = translated_text
    # Przekierowanie z powrotem do strony głównej
    return redirect(url_for('translator'))

@app.route("/slownik", methods=["GET", "POST"])
def display_dictionary():
    global translation_dictionary
    # Pobieranie wybranego języka źródłowego z formularza
    selected_lang = request.form.get("selected_lang", "pl")

    if selected_lang:
        # Filtrowanie słownika według wybranego języka źródłowego
        filtered_dict = {k: v for k, v in translation_dictionary.items() if detect(k) == selected_lang}
    else:
        # Wyświetlanie pełnego słownika
        filtered_dict = translation_dictionary

    # Renderowanie szablonu słownika
    return render_template("slownik.html", slownik=filtered_dict, selected_lang=selected_lang, supported_languages=SUPPORTED_LANGUAGES)

if __name__ == "__main__":
    # Uruchomienie aplikacji w trybie debugowania
    app.run(debug=True)
