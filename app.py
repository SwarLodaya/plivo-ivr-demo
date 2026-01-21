from flask import Flask, request, Response, render_template
import plivo
from plivo import plivoxml
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BASE_URL = "https://nonpaternally-overcopious-mathias.ngrok-free.dev"

# ---------------- HOME + UI ----------------

@app.route("/")
def home():
    return "Plivo IVR Demo is running!"

@app.route("/ui")
def ui():
    return render_template("index.html")

# ---------------- OUTBOUND CALL ----------------

@app.route("/call", methods=["POST"])
def make_call():
    client = plivo.RestClient(
        os.getenv("PLIVO_AUTH_ID"),
        os.getenv("PLIVO_AUTH_TOKEN")
    )

    from_number = os.getenv("PLIVO_FROM_NUMBER")
    data = request.get_json(force=True)
    to_number = data.get("to")

    response = client.calls.create(
        from_=from_number,
        to_=to_number,
        answer_url=f"{BASE_URL}/ivr-level-1",
        answer_method="GET"
    )

    return {"message": "Call initiated", "call_uuid": response["request_uuid"]}

# ---------------- LEVEL 1 ----------------

@app.route("/ivr-level-1", methods=["GET", "POST"])
def ivr_level_1():
    response = plivoxml.ResponseElement()

    get_digits = plivoxml.GetDigitsElement(
        action=f"{BASE_URL}/ivr-level-2",
        method="POST",
        timeout=10,
        num_digits=1,
        retries=1
    )

    get_digits.add(plivoxml.SpeakElement("Press 1 for English. Press 2 for Spanish."))
    response.add(get_digits)

    response.add(plivoxml.SpeakElement("Invalid or no input. Repeating the menu."))
    response.add(plivoxml.RedirectElement(f"{BASE_URL}/ivr-level-1"))

    return Response(response.to_string(), mimetype="text/xml")

# ---------------- LEVEL 2 ----------------

@app.route("/ivr-level-2", methods=["POST"])
def ivr_level_2():
    digit = request.form.get("Digits")
    response = plivoxml.ResponseElement()

    if digit == "1":
        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/english-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Press 1 to hear a message. Press 2 to talk to an agent."))
        response.add(get_digits)

        response.add(plivoxml.SpeakElement("Invalid or no input. Repeating the menu."))
        response.add(plivoxml.RedirectElement(f"{BASE_URL}/english-menu"))

    elif digit == "2":
        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/spanish-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Presione 1 para escuchar un mensaje. Presione 2 para hablar con un agente."))
        response.add(get_digits)

        response.add(plivoxml.SpeakElement("Entrada no válida. Repitiendo el menú."))
        response.add(plivoxml.RedirectElement(f"{BASE_URL}/spanish-menu"))

    else:
        response.add(plivoxml.SpeakElement("Invalid input. Repeating this menu."))
        response.add(plivoxml.RedirectElement(f"{BASE_URL}/ivr-level-1"))

    return Response(response.to_string(), mimetype="text/xml")

# ---------------- ENGLISH MENU ----------------

@app.route("/english-menu", methods=["POST"])
def english_menu():
    digit = request.form.get("Digits")
    response = plivoxml.ResponseElement()

    if digit == "1":
        response.add(plivoxml.PlayElement(
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ))

        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/english-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Press 1 to hear the message again. Press 2 to talk to an agent."))
        response.add(get_digits)

    elif digit == "2":
        response.add(plivoxml.SpeakElement("Connecting you to a live agent. Please hold."))

        dial = plivoxml.DialElement(timeout=20)
        dial.add(plivoxml.NumberElement("918147721290"))
        response.add(dial)

        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/english-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("The agent is unavailable. Press 1 to hear the message. Press 2 to try again."))
        response.add(get_digits)

    else:
        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/english-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Invalid input. Press 1 to hear the message. Press 2 to talk to an agent."))
        response.add(get_digits)

    return Response(response.to_string(), mimetype="text/xml")

# ---------------- SPANISH MENU ----------------

@app.route("/spanish-menu", methods=["POST"])
def spanish_menu():
    digit = request.form.get("Digits")
    response = plivoxml.ResponseElement()

    if digit == "1":
        response.add(plivoxml.PlayElement(
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ))

        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/spanish-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Presione 1 para escuchar de nuevo. Presione 2 para hablar con un agente."))
        response.add(get_digits)

    elif digit == "2":
        response.add(plivoxml.SpeakElement("Conectando con un agente en vivo. Por favor espere."))

        dial = plivoxml.DialElement(timeout=20)
        dial.add(plivoxml.NumberElement("918147721290"))
        response.add(dial)

        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/spanish-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("El agente no está disponible. Presione 1 para escuchar el mensaje. Presione 2 para intentar otra vez."))
        response.add(get_digits)

    else:
        get_digits = plivoxml.GetDigitsElement(
            action=f"{BASE_URL}/spanish-menu",
            method="POST",
            timeout=10,
            num_digits=1,
            retries=1
        )
        get_digits.add(plivoxml.SpeakElement("Entrada no válida. Presione 1 para escuchar el mensaje. Presione 2 para hablar con un agente."))
        response.add(get_digits)

    return Response(response.to_string(), mimetype="text/xml")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)

