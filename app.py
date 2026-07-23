from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "smk-mobiles-photography-2026"
app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "images", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "products.json"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def load_products() -> List[Dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_products(products: List[Dict[str, Any]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(products, handle, indent=2)


def save_uploaded_image(file_storage) -> str | None:
    if file_storage is None or file_storage.filename == "":
        return None

    filename = secure_filename(file_storage.filename)
    if not filename:
        return None

    ext = os.path.splitext(filename)[1].lower()
    if ext not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        raise ValueError("Only image files are allowed.")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(file_path)
    return f"/static/images/uploads/{unique_name}"


@app.context_processor
def inject_globals() -> Dict[str, Any]:
    return {
        "business_name": "SMK Mobiles & Photography",
        "address": "17/2, West Main Street, Thiruvaiyaru",
        "phone": "8608263979",
        "phone2": "9789373153",
        "whatsapp": "8608263979",
        "email": "smkmobiles@gmail.com",
        "year": datetime.now().year,
    }


@app.route("/")
def index() -> str:
    products = load_products()[:8]
    return render_template("index.html", products=products)


@app.route("/about")
def about() -> str:
    return render_template("about.html")


@app.route("/products")
def products() -> str:
    products = load_products()
    search = request.args.get("search", "", type=str).strip()
    brand = request.args.get("brand", "", type=str).strip()

    if search:
        search_lower = search.lower()
        products = [
            product
            for product in products
            if search_lower in product.get("name", "").lower()
            or search_lower in product.get("brand", "").lower()
            or search_lower in product.get("description", "").lower()
        ]

    if brand:
        products = [
            product for product in products if brand.lower() in product.get("brand", "").lower()
        ]

    brands = sorted({product.get("brand", "") for product in products if product.get("brand")})
    return render_template("products.html", products=products, brands=brands, search=search, brand=brand)


@app.route("/services")
def services() -> str:
    services = [
        {"title": "Mobile Sales", "desc": "Premium flagship, budget, and business smartphones.", "icon": "fas fa-mobile-alt"},
        {"title": "Mobile Accessories", "desc": "Covers, chargers, earbuds, power banks and more.", "icon": "fas fa-headphones"},
        {"title": "Mobile Repair", "desc": "Screen, battery, speaker, and motherboard repair support.", "icon": "fas fa-tools"},
        {"title": "Mobile Exchange", "desc": "Upgrade smoothly with value-based exchange offers.", "icon": "fas fa-sync-alt"},
        {"title": "Used Mobiles", "desc": "Quality tested used phones with warranty and support.", "icon": "fas fa-box-open"},
        {"title": "Photography & Printing", "desc": "Wedding, portrait, temple and passport photography.", "icon": "fas fa-camera"},
    ]
    return render_template("services.html", services=services)


@app.route("/gallery")
def gallery() -> str:
    images = [
        {"title": "Wedding Shoot", "url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=800&q=80"},
        {"title": "Portrait Session", "url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=800&q=80"},
        {"title": "Temple Photography", "url": "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=800&q=80"},
        {"title": "Outdoor Campaign", "url": "https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&fit=crop&w=800&q=80"},
        {"title": "Passport Photos", "url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"},
        {"title": "Printing Studio", "url": "https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=800&q=80"},
    ]
    return render_template("gallery.html", images=images)


@app.route("/offers")
def offers() -> str:
    offers = [
        {"title": "Today's Deals", "desc": "Limited-time price drops on latest flagship mobiles and accessories."},
        {"title": "Festival Offers", "desc": "Special festive bundles with premium gifting options."},
        {"title": "Student Discounts", "desc": "Exclusive discounts for students and education professionals."},
        {"title": "Accessories Combo", "desc": "Save more with curated accessory bundles and service plans."},
    ]
    return render_template("offers.html", offers=offers)


@app.route("/brands")
def brands() -> str:
    brand_items = [
        "Apple", "Samsung", "Vivo", "Oppo", "Realme", "OnePlus", "Nothing", "Motorola",
        "Redmi", "POCO", "Google Pixel", "Nokia", "Honor", "Infinix", "Tecno"
    ]
    return render_template("brands.html", brands=brand_items)


@app.route("/testimonial")
def testimonial() -> str:
    testimonials = [
        {"name": "Ravi Kumar", "place": "Thiruvaiyaru", "quote": "Excellent service and genuine pricing. I bought my iPhone here and the support was outstanding.", "rating": 5},
        {"name": "Karthik", "place": "Kumbakonam", "quote": "Fast repair service and amazing photography package for my wedding. Highly recommended!", "rating": 5},
        {"name": "Sangeetha", "place": "Tanjore", "quote": "Professional staff and polished experience. Their exchange offers were very helpful.", "rating": 5},
    ]
    return render_template("testimonial.html", testimonials=testimonials)


@app.route("/faq")
def faq() -> str:
    faqs = [
        {"question": "Do you sell both new and used mobiles?", "answer": "Yes, we offer quality-assured new and used phones with warranty support."},
        {"question": "Do you provide repair services?", "answer": "We handle screen, battery, charging, software, and hardware repairs."},
        {"question": "Can I exchange my old phone?", "answer": "Yes, we provide exchange options based on model condition and market value."},
        {"question": "Do you offer photography services?", "answer": "We provide wedding, portrait, temple, outdoor, passport photography and printing."},
    ]
    return render_template("faq.html", faqs=faqs)


@app.route("/contact", methods=["GET", "POST"])
def contact() -> str | Any:
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all contact fields.", "error")
        else:
            flash("Your message has been received. We will contact you soon.", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Any:
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))

        flash("Invalid admin credentials.", "error")

    return render_template("admin/login.html")


@app.route("/dashboard")
def dashboard() -> str | Any:
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    products = load_products()
    return render_template("admin/dashboard.html", products=products)


@app.route("/add-product", methods=["GET", "POST"])
def add_product() -> str | Any:
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            image_url = save_uploaded_image(request.files.get("image"))
        except ValueError as exc:
            flash(str(exc), "error")
            return render_template("admin/add-product.html")

        product = {
            "id": uuid.uuid4().hex[:8],
            "name": request.form.get("name", "").strip(),
            "brand": request.form.get("brand", "").strip(),
            "price": int(request.form.get("price", 0)),
            "offer_price": int(request.form.get("offer_price", 0)),
            "availability": request.form.get("availability", "In Stock"),
            "description": request.form.get("description", ""),
            "image": image_url or request.form.get("image_url", "/static/images/placeholder.jpg"),
            "category": request.form.get("category", "Mobile"),
        }

        products = load_products()
        products.append(product)
        save_products(products)
        flash("Product added successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("admin/add-product.html")


@app.route("/edit-product/<product_id>", methods=["GET", "POST"])
def edit_product(product_id: str) -> str | Any:
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    products = load_products()
    product = next((item for item in products if item.get("id") == product_id), None)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        try:
            image_url = save_uploaded_image(request.files.get("image"))
        except ValueError as exc:
            flash(str(exc), "error")
            return render_template("admin/edit-product.html", product=product)

        product["name"] = request.form.get("name", "").strip()
        product["brand"] = request.form.get("brand", "").strip()
        product["price"] = int(request.form.get("price", 0))
        product["offer_price"] = int(request.form.get("offer_price", 0))
        product["availability"] = request.form.get("availability", "In Stock")
        product["description"] = request.form.get("description", "")
        product["category"] = request.form.get("category", "Mobile")
        if image_url:
            product["image"] = image_url
        elif request.form.get("image_url"):
            product["image"] = request.form.get("image_url")

        save_products(products)
        flash("Product updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("admin/edit-product.html", product=product)


@app.route("/delete-product/<product_id>", methods=["POST"])
def delete_product(product_id: str) -> Any:
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    products = load_products()
    products = [item for item in products if item.get("id") != product_id]
    save_products(products)
    flash("Product deleted successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout() -> Any:
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
