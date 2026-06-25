from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion leida de variables de entorno / fichero .env."""

    # Busca .env en el cwd y en la raiz del proyecto (un nivel por encima de
    # backend/), util para ejecutar uvicorn en local sin Docker.
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    # Clave de Google Maps (Geocoding + Distance Matrix). Se mantiene en el
    # backend para no exponerla en el navegador.
    google_maps_api_key: str = ""

    # Origenes permitidos para CORS (frontend). Separados por comas.
    cors_origins: str = "http://localhost:5173,http://localhost:4173"

    # Maximo de centros que se devuelven en una consulta.
    max_results: int = 800

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
