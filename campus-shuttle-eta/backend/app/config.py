import os

class Settings:
    PROJECT_NAME: str = "ShuttleSense H4 Predictive ETA"
    CAMPUS_NAME: str = "Central Tech Campus"
    CENTER_LAT: float = 31.2548
    CENTER_LNG: float = 75.7052
    MAX_GPS_ACCURACY_M: float = float(os.getenv("MAX_GPS_ACCURACY_M", "65.0"))
    MAX_SPEED_KMH: float = float(os.getenv("MAX_SPEED_KMH", "80.0"))
    DROPOUT_TOLERANCE_SEC: float = float(os.getenv("DROPOUT_TOLERANCE_SEC", "120.0"))
    ACCURACY_TARGET_WINDOW_SEC: float = 120.0  # ±2 min target
    ACCURACY_TARGET_RATIO: float = 0.80        # ≥ 80%

settings = Settings()
