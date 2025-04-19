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
    # ... (remaining barbers unchanged)
]

blogs = [
    {
        "id": 1,
        "title": "Welcome to BarberScout Amsterdam",
        "slug": "welcome-to-barberscout",
        "author": "Team BarberScout",
        "date": "2025-04-19",
        "city": "amsterdam",
        "image_url": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/BarberScout%20Logo%20v2-egYCXVrjwzUdVSDJ1RYpij2xBGbUbK.png",
        "content": """
Finding a great barber is personal.  
Finding one who gets your style and speaks your language? That can be a mission — especially in a city as international as Amsterdam.

That's where BarberScout comes in.

We're building Amsterdam's first dedicated directory of **English-speaking** and **walk-in friendly** barbershops, so you can stop guessing, scrolling, or settling for whatever’s closest. Whether you're new to the city, visiting for a few weeks, or just looking for a fresh fade without the language barrier — we've got you.

### Why We Started BarberScout

After countless awkward haircuts and “lost in translation” appointments, we realized something:  
There’s no central place to find barbers who speak English and deliver sharp, consistent results.

So we decided to build one.

BarberScout is here to:

✅ Help you find reliable, English-speaking barbers in your neighborhood  
✅ Make it easy to see services, prices, and availability — all in one place  
✅ Support local barbers by giving them the visibility they deserve  

### What's Live Now (And What's Coming)

Right now, we’re focused on Amsterdam.  
You’ll find a growing list of English-speaking barbers with verified info and direct booking links.

Coming soon:

💳 Featured listings for barbers who want to stand out  
💬 Real reviews from the local community  
✈️ Expansion to other major cities across Europe  

### Are You a Barber?

We’d love to feature you — especially if your barbershop:

- Speaks English fluently  
- Offers consistent, high-quality cuts  
- Welcomes walk-ins or same-day appointments  
- Wants to reach more international clients

👉 Submit your details here.  
It’s free to get listed, and we’ll do the heavy lifting to get you noticed.

### Help Us Grow

BarberScout is brand new — and your support means the world.

Here’s how you can help:

💈 Know a great barbershop? Tell them to get listed  
📣 Share this site with friends and expats in Amsterdam  
🌍 Follow us on socials for updates, new listings, and barber spotlights

Thanks for being here — we’re just getting started.  
Stay fresh,  
**The BarberScout Team**

✂️ [www.barberscout.co](https://www.barberscout.co)
        """
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

@app.route("/blogs", methods=["GET"])
def get_blogs():
    return jsonify(blogs)

@app.route("/blogs/<slug>", methods=["GET"])
def get_blog_by_slug(slug):
    blog = next((b for b in blogs if b["slug"] == slug), None)
    if blog:
        return jsonify(blog)
    return jsonify({"error": "Blog not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
