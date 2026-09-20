from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

api_bp = Blueprint("api", __name__, url_prefix="/api")
pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    veri = request.get_json()
    mesaj = veri.get("mesaj")
    gecmis = veri.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj zorunludur."
        }), 400

    try:
            cevap = ai_service.yanit_uret(mesaj, gecmis)

            return jsonify({
                "basari": True,
                "cevap": cevap
            }), 200

    except AIServiceError as e:
            return jsonify({
                "basari": False,
                "hata": str(e)
            }), 503   

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