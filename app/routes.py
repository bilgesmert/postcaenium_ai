from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler

api_bp = Blueprint("api", __name__, url_prefix="/api")
pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    veri = request.get_json()
    isim = veri.get("isim")
    telefon = veri.get("telefon")
    mesaj = veri.get("mesaj")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon zorunludur."
        }), 400

    lead_ekle(isim, telefon, mesaj)

    return jsonify({
        "basari": True,
        "mesaj": "Lead başarıyla kaydedildi."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def leadleri_listele():
    leadler = tum_leadler()

    return jsonify({
        "basari": True,
        "leadler": leadler
    }), 200