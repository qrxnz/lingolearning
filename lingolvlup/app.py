import requests
from flask import Flask, render_template, request, make_response, redirect, url_for
from dotenv import load_dotenv
import os
from langdetect import detect, LangDetectException
import secrets
import os

load_dotenv()

app = Flask(__name__)
API_URL = "https://text-translator2.p.rapidapi.com/translate"
API_KEY = os.getenv("X_RAPIDAPI_KEY")
SUPPORTED_LANGUAGES = ["es", "fr", "de", "en", "pl"]

app.secret_key = secrets.token_urlsafe(32)

# Zmienna globalna do przechowywania słownika
translation_dictionary = {}

@app.route("/", methods=["GET", "POST"])
def translator():
    if request.method == "POST":
        text = request.form["text"]
        target_lang = request.form["target_lang"]

        # Wykrywanie języka źródłowego
        try:
            source_lang = detect(text)
        except LangDetectException:
            source_lang = "pl"  # Default to Polish if detection fails

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }

        payload = f"source_language={source_lang}&target_language={target_lang}&text={text}"

        response = requests.post(API_URL, data=payload, headers=headers)

        if response.status_code == 200:
            translated_text = response.json()["data"]["translatedText"]
            resp = make_response(render_template("translator.html", translated_text=translated_text, source_lang=source_lang, target_lang=target_lang, supported_languages=SUPPORTED_LANGUAGES))
            resp.set_cookie("target_lang", target_lang)
            return resp
        else:
            return render_template("translator.html", error="Błąd tłumaczenia.", supported_languages=SUPPORTED_LANGUAGES)

    target_lang = request.cookies.get("target_lang", SUPPORTED_LANGUAGES[0])
    return render_template("translator.html", target_lang=target_lang, supported_languages=SUPPORTED_LANGUAGES)

@app.route("/save_translation", methods=["POST"])
def save_translation():
    global translation_dictionary
    source_text = request.form["source_text"]
    translated_text = request.form["translated_text"]
    translation_dictionary[source_text] = translated_text
    return redirect(url_for('translator'))

@app.route("/slownik", methods=["GET", "POST"])
def display_dictionary():
    global translation_dictionary
    selected_lang = request.form.get("selected_lang", "pl")

    if selected_lang:
        filtered_dict = {k: v for k, v in translation_dictionary.items() if detect(k) == selected_lang}
    else:
        filtered_dict = translation_dictionary

    return render_template("slownik.html", slownik=filtered_dict, selected_lang=selected_lang, supported_languages=SUPPORTED_LANGUAGES)

if __name__ == "__main__":
    app.run(debug=True)
