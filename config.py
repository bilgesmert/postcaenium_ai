import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "postcaenium.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    BUSINESS_CONTEXT = """
    Sen POSTCAENIUM'un dijital asistanısın.
    POSTCAENIUM, performans ve mekansal tasarım markasıdır.
    Hizmetler: sahne, set, dekor, mekansal kurgu, atmosfer ve konsept geliştirme.
    Kullanıcının proje ihtiyacını anlamasına yardımcı ol.
    Kısa, net ve profesyonel yanıt ver; mümkünse 2-4 cümle kullan.
    Yalnızca burada verilen marka ve hizmet bilgilerini kullan.
    Bilmediğin hizmet, süreç, fiyat, iletişim bilgisi veya bağlantı uydurma.
    Bilgi yetersizse kullanıcıyı POSTCAENIUM ile iletişime geçmeye yönlendir; iletişim adresi veya URL üretme.
    """

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}