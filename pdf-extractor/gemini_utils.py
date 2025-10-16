import os
from google import genai

# API-Key setzen
os.environ["GEMINI_API_KEY"] = "the_api_key"

# Client initialisieren
client = genai.Client()

# Anfrage an das Modell stellen
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Erkläre in wenigen Worten, wie KI funktioniert"
)

# Antwort ausgeben
print(response.text)
