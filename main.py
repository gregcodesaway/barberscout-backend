from flask import Flask, jsonify, request
from flask_cors import CORS
from difflib import SequenceMatcher
import os

app = Flask(__name__)
CORS(app)

barbers = [
    {
        "id": 1,
        "name": "BRUHN Barbershop",
        "address": "Albert Cuypstraat 156E, 1073 BK Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Styling", "Fade"],
        "rating": 4.8,
        "speaks_english": True,
        "opening_hours": "Mon: 10:00–19:00, Tue: 12:00–20:00, Wed–Fri: 08:20–21:00, Sat: 09:00–19:00, Sun: 12:00–20:00",
        "contact": "https://www.bruhn.nl",
        "image_url": "https://cdn.prod.website-files.com/642843be0da449a9eaf4accd/651c1dfdaaca2da0c4742ec0_IMG_0392-p-500.webp"
    },
    {
        "id": 2,
        "name": "Prime Barbershop",
        "address": "Nieuwendijk 85, 1012 MC Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hair Coloring", "Fade"],
        "rating": 4.9,
        "speaks_english": True,
        "opening_hours": "Mon–Sun: 09:30–20:00",
        "contact": "https://primebarbershop.nl",
        "image_url": "https://primebarbershop.nl/wp-content/uploads/2023/09/cropped-Prime-Barber-shop-01.png"
    },
    {
        "id": 3,
        "name": "City Center Barbershop",
        "address": "Stationsplein 41M, 1012 AB Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Fade"],
        "rating": 4.6,
        "speaks_english": True,
        "opening_hours": "Mon–Fri: 08:00–21:00, Sat: 09:00–20:00, Sun: 10:00–20:00",
        "contact": "https://citycenterbarbershop.nl",
        "image_url": "https://citycenterbarbershop.nl/wp-content/uploads/2024/03/citycenterbarber-white-1.webp"
    },
    {
        "id": 4,
        "name": "Cut Throat Amsterdam",
        "address": "Beursplein 5, 1012 JW Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Facial", "Fade"],
        "rating": 4.7,
        "speaks_english": True,
        "opening_hours": "Mon: 09:00–19:00, Tue: 09:00–21:00, Wed–Thu: 09:00–20:00, Fri: 08:00–19:00, Sat: 08:00–18:00, Sun: 11:00–18:00",
        "contact": "https://cutthroatbarber.nl",
        "image_url": "http://cutthroatbarber.nl/wp-content/uploads/2022/05/cutthroat-logo.png"
    }
]

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.6

@app.route("/barbers", methods=["GET"])
def get_barbers():
    query = request.args.get("q", "").lower()

    if query:
        results = []
        for barber in barbers:
            if (
                similar(query, barber["name"]) or
                similar(query, barber["address"]) or
                any(similar(query, service) for service in barber["services"])
            ):
                results.append(barber)
        return jsonify(results)

    return jsonify(barbers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # <-- This fixes the Render port binding issue
    app.run(host="0.0.0.0", port=port)
