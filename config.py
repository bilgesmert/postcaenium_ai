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
    POSTCAENIUM, performans ve mekansal tasarım alanında çalışan bir tasarım markasıdır.
    Marka; sahne, set, dekor, mekansal kurgu, atmosfer ve konsept geliştirme alanlarında hizmet verir.
    Ziyaretçilere POSTCAENIUM'un hizmetleri hakkında açık, profesyonel ve kısa bilgiler ver.
    Kullanıcının proje ihtiyacını anlamasına yardımcı ol.
    Bilmediğin proje detaylarını uydurma.
    Gerekli durumlarda kullanıcıyı POSTCAENIUM ile iletişime geçmeye yönlendir.
    """

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}