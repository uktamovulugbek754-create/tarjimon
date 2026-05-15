from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()


def check_groq_limits():
    api_key = os.environ.get("GROQ_API_KEY")

    print("=" * 55)
    print("       GROQ API HOLATI TEKSHIRUVI")
    print("=" * 55)
    print(f"⏰  Vaqt    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if not api_key:
        print("❌  GROQ_API_KEY topilmadi. .env faylni tekshiring.")
        print("=" * 55)
        return

    print(f"🔑  API kalit: {api_key[:20]}...")
    print("=" * 55)

    client = Groq(api_key=api_key)

    # ── Test 1: Chat API ──────────────────────────────────────
    print("\n📡  Test 1 — Chat API:")
    try:
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
        )
        print("   ✅  Chat API ishlayapti")
    except Exception as e:
        msg = str(e)
        if "429" in msg or "rate limit" in msg.lower():
            print("   ⚠️   Rate limit! Cheklov kutilmoqda (1 daqiqa kuting)")
        else:
            print(f"   ❌  Xato: {msg[:120]}")

    # ── Test 2: Mavjud modellar ───────────────────────────────
    print("\n📋  Test 2 — Mavjud modellar:")
    try:
        models = client.models.list()
        names  = [m.id for m in models.data]
        print(f"   ✅  Jami {len(names)} ta model topildi")
        print("   🔹  Dastlabki 5 ta:")
        for name in sorted(names)[:5]:
            print(f"       • {name}")
    except Exception as e:
        print(f"   ❌  Modellar ro'yxati olinmadi: {str(e)[:120]}")

    # ── Free tier chegaralari ─────────────────────────────────
    print("\n📊  Groq Free Tier chegaralari:")
    print("   ┌─────────────────────────────────────────┐")
    print("   │  RPM  (daqiqada so'rovlar)  :     30    │")
    print("   │  RPD  (kundalik so'rovlar)  :  14,400   │")
    print("   │  TPM  (daqiqada tokenlar)   :   6,000   │")
    print("   │  Audio fayl hajmi (max)     :    25 MB  │")
    print("   └─────────────────────────────────────────┘")

    # ── Foydali eslatmalar ────────────────────────────────────
    print("\n💡  Eslatmalar:")
    print("   • 429 xatosi chiqsa — 1 daqiqa kuting, so'ng qayta urining")
    print("   • Kunlik limit UTC 00:00 da yangilanadi (O'zbekiston +5)")
    print("   • Batafsil: https://console.groq.com/settings/limits")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    check_groq_limits()
