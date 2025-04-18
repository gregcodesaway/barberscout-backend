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
        "city": "amsterdam",
        "address": "Albert Cuypstraat 156E, 1073 BK Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Styling", "Fade", "Skin Fade"],
        "rating": 4.7,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": False,
        "opening_hours": "Mon: 10:00–19:00, Tue: 12:00–20:00, Wed–Fri: 08:20–21:00, Sat: 09:00–19:00, Sun: 12:00–20:00",
        "contact": "https://www.bruhn.nl",
        "image_url": "https://cdn.prod.website-files.com/642843be0da449a9eaf4accd/651c1dfdaaca2da0c4742ec0_IMG_0392-p-500.webp"
    },
    {
        "id": 2,
        "name": "Prime Barbershop",
        "city": "amsterdam",
        "address": "Nieuwendijk 85, 1012 MC Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hair Coloring", "Fade", "Skin Fade", "Walk-ins"],
        "rating": 4.9,
        "speaks_english": True,
        "walk_ins": True,
        "student_discount": False,
        "opening_hours": "Mon–Sun: 09:30–20:00",
        "contact": "https://primebarbershop.nl",
        "image_url": "https://primebarbershop.nl/wp-content/uploads/2023/09/cropped-Prime-Barber-shop-01.png"
    },
    {
        "id": 3,
        "name": "City Center Barbershop",
        "city": "amsterdam",
        "address": "Stationsplein 41M, 1012 AB Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Fade", "Skin Fade"],
        "rating": 4.9,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": False,
        "opening_hours": "Mon–Fri: 08:00–21:00, Sat: 09:00–20:00, Sun: 10:00–20:00",
        "contact": "https://citycenterbarbershop.nl",
        "image_url": "https://citycenterbarbershop.nl/wp-content/uploads/2024/03/citycenterbarber-white-1.webp"
    },
    {
        "id": 4,
        "name": "Cut Throat Amsterdam",
        "city": "amsterdam",
        "address": "Beursplein 5, 1012 JW Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Facial", "Fade", "Skin Fade", "Hair wash"],
        "rating": 4.6,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": True,
        "opening_hours": "Mon: 09:00–19:00, Tue: 09:00–21:00, Wed–Thu: 09:00–20:00, Fri: 08:00–19:00, Sat: 08:00–18:00, Sun: 11:00–18:00",
        "contact": "https://cutthroatbarber.nl",
        "image_url": "http://cutthroatbarber.nl/wp-content/uploads/2022/05/cutthroat-logo.png"
    },
    {
        "id": 5,
        "name": "Rogue Razor Barbershop",
        "city": "amsterdam",
        "address": "Mauritskade 112 H, 1093 RT, Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Fade", "Skin Fade", "Q-Ball", "Hair wash"],
        "rating": 4.8,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": True,
        "opening_hours": "Mon: CLOSED, Tue: 10:00–19:00, Wed–Thu: 11:00–20:00, Fri: 10:00–18:30, Sat: 10:00–18:30, Sun: CLOSED",
        "contact": "https://roguerazor.nl/",
        "image_url": "https://impro.usercontent.one/appid/oneComWsb/domain/roguerazor.nl/media/roguerazor.nl/onewebmedia/RR-logo-new___serialized1.png"
    },
    {
        "id": 6,
        "name": "Mr Elias Barbershop",
        "city": "amsterdam",
        "address": "Linnaeusstraat 60h, 1092 CM, Amsterdam",
        "services": ["Haircut", "Beard Trim", "Hot Towel Shave", "Fade", "Skin Fade", "Buzz Cut", "Hair wash"],
        "rating": 4.9,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": False,
        "opening_hours": "Mon-Fri: 10:00–18:30, Sat: 09:30–18:30, Sun: CLOSED",
        "contact": "https://mrelias.nl/",
        "image_url": "https://mrelias.nl/wp-content/uploads/2020/11/logo.png"
    },
    {
        "id": 7,
        "name": "HIS Amsterdam",
        "city": "amsterdam",
        "address": "Utrechtsedwarsstraat 86, 1017 WH Amsterdam",
        "services": ["Beard Trim", "Haircut", "Hot Towel", "Facial", "Beard Colouring", "Eye Mask", "Face Mask", "Peel Mask", "Body Wax"],
        "rating": 4.5,
        "speaks_english": True,
        "walk_ins": False,
        "student_discount": False,
        "opening_hours": "Mon: Closed, Tues: 10:00–19:00, Weds: 10:00–19:00, Thurs: 10:00–21:00, Fri: 10:00–19:00, Sat: 10:00–19:00, Sun: 12:00–19:00",
        "contact": "https://www.hisamsterdam.nl",
        "image_url": "https://www.hisamsterdam.nl/wp-content/uploads/2023/02/his-amsterdam-logo-new-02.svg"
    }
]

def matches_query(query, text):
    query = query.lower()
    text = text.lower()
    if query in text:
        return True
    for word in query.split():
        if word in text or SequenceMatcher(None, word, text).ratio() > 0.75:
            return True
    return False

@app.route("/barbers", methods=["GET"])
def get_barbers():
    query = request.args.get("q", "").strip().lower()
    city = request.args.get("city", "").strip().lower()

    results = []
    for barber in barbers:
        if city and barber.get("city", "").lower() != city:
            continue
        if not query or (
            matches_query(query, barber["name"]) or
            matches_query(query, barber["address"]) or
            any(matches_query(query, service) for service in barber["services"])
        ):
            results.append(barber)

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
