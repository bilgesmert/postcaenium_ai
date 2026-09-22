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

    if not isinstance(gecmis, list):
        return jsonify({
            "basari": False,
            "hata": "Geçmiş bilgisi liste formatında olmalıdır."
        }), 400

    for kayit in gecmis:
        if (
            not isinstance(kayit, dict)
            or kayit.get("role") not in ["user", "assistant"]
            or not isinstance(kayit.get("content"), str)
            or not kayit.get("content").strip()
        ):
            return jsonify({
                "basari": False,
                "hata": "Geçmiş konuşma formatı geçersiz."
            }), 400

    if not isinstance(mesaj, str) or not mesaj.strip():
        return jsonify({
            "basari": False,
            "hata": "Mesaj zorunludur."
        }), 400

    if len(mesaj) > 2000:
        return jsonify({
            "basari": False,
            "hata": "Mesaj en fazla 2000 karakter olabilir."
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

    if not isinstance(isim, str) or not isim.strip():
        return jsonify({
            "basari": False,
            "hata": "Geçerli bir isim girilmelidir."
        }), 400

    if len(isim.strip()) > 100:
        return jsonify({
            "basari": False,
            "hata": "İsim en fazla 100 karakter olabilir."
        }), 400

    if not isinstance(telefon, str) or not telefon.strip():
        return jsonify({
            "basari": False,
            "hata": "Geçerli bir telefon numarası girilmelidir."
        }), 400

    if len(telefon.strip()) > 30:
        return jsonify({
            "basari": False,
            "hata": "Telefon numarası en fazla 30 karakter olabilir."
        }), 400

    if mesaj is not None and not isinstance(mesaj, str):
        return jsonify({
            "basari": False,
            "hata": "Mesaj metin formatında olmalıdır."
        }), 400

    if isinstance(mesaj, str) and len(mesaj.strip()) > 2000:
        return jsonify({
            "basari": False,
            "hata": "Mesaj en fazla 2000 karakter olabilir."
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