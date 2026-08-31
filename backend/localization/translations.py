from typing import Dict, Any


class LocalizationManager:
    TRANSLATIONS: Dict[str, Dict[str, str]] = {
        "en": {
            "app_title": "Velocity Nexus",
            "play_race": "Start Race",
            "garage": "Garage Showroom",
            "customization": "Visual Customization",
            "career": "Career Mode",
            "ranked": "Ranked Ladder",
            "leaderboards": "Global Leaderboards",
            "credits": "Credits",
            "nexus_gold": "Nexus Gold",
            "speed": "Speed",
            "gear": "Gear",
            "lap": "Lap",
            "position": "Position",
            "driver_dna": "Driver DNA Profile",
            "login": "Quick Login"
        },
        "te": {
            "app_title": "వెలొసిటీ నెక్సస్",
            "play_race": "రేస్ ప్రారంభించు",
            "garage": "గ్యారేజ్ షోరూమ్",
            "customization": "వాహన అనుకూలీకరణ",
            "career": "కెరీర్ మోడ్",
            "ranked": "ర్యాంక్డ్ పోటీ",
            "leaderboards": "లీడర్‌బోర్డులు",
            "credits": "క్రెడిట్స్",
            "nexus_gold": "నెక్సస్ గోల్డ్",
            "speed": "వేగం",
            "gear": "గేర్",
            "lap": "ల్యాప్",
            "position": "స్థానం",
            "driver_dna": "డ్రైవర్ DNA ప్రొఫైల్",
            "login": "త్వరిత లాగిన్"
        },
        "hi": {
            "app_title": "वेलोसिटी नेक्सस",
            "play_race": "दौड़ शुरू करें",
            "garage": "गैराज शोरूम",
            "customization": "वाहन अनुकूलन",
            "career": "करियर मोड",
            "ranked": "रैंक्ड मैच",
            "leaderboards": "लीडरबोर्ड",
            "credits": "क्रेडिट्स",
            "nexus_gold": "नेक्सस गोल्ड",
            "speed": "गति",
            "gear": "गियर",
            "lap": "लैप",
            "position": "स्थान",
            "driver_dna": "ड्राइवर डीएनए",
            "login": "त्वरित लॉगिन"
        },
        "ta": {
            "app_title": "வெலாசிட்டி நெக்ஸஸ்",
            "play_race": "பந்தயத்தைத் தொடங்கு",
            "garage": "கேரேஜ் ஷோரூம்",
            "customization": "தனிப்பயனாக்கம்",
            "career": "தொழில் முறை",
            "ranked": "தரவரிசை போட்டி",
            "leaderboards": "முன்னணி பட்டியல்",
            "credits": "கிரெடிட்கள்",
            "nexus_gold": "நெக்ஸஸ் தங்கம்",
            "speed": "வேகம்",
            "gear": "கியர்",
            "lap": "சுற்று",
            "position": "நிலை",
            "driver_dna": "டிரைவர் டி.என்.ஏ",
            "login": "உள்நுழைக"
        }
    }

    @classmethod
    def get_text(cls, key: str, lang: str = "en") -> str:
        lang_dict = cls.TRANSLATIONS.get(lang, cls.TRANSLATIONS["en"])
        return lang_dict.get(key, cls.TRANSLATIONS["en"].get(key, key))
