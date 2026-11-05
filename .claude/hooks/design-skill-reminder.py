#!/usr/bin/env python3
"""PreToolUse hook: before a mutating use_figma call, remind to state which
design skill drives each design decision. Non-blocking: it only injects
context. Read-only calls are skipped. Any error exits 0 silently so it can
never stall the work."""
import json
import sys

MUTATING_HINTS = (
    "create", "appendChild", ".fills", ".strokes", ".name =", "resize(",
    ".remove()", "setBoundVariable", "layoutMode", "characters =", ".set(",
)

REMINDER = (
    "תזכורת עיצוב (design-routing): לפני הכתיבה ל־Figma ציין לכל החלטה עיצובית "
    "שורה אחת בפורמט 'החלטה <- סקיל/כלל'. סדר עדיפויות: כללי המוצר, figma-use / "
    "figma-generate-*, נגישות (ui-ux-pro-max), ורק אז אסתטיקה (frontend-design, "
    "taste-skill). אם אין סקיל רלוונטי כתוב 'ללא סקיל - הנחה שלי' וסמן מוצע. "
    "כיוון חזותי: IBM Plex Sans Hebrew לכותרות + Assistant לגוף (אושר). פלטה: מרווה ודיו (אושר 5.11); זהב נדחה, צבע נגיעה כחול ערפל (אושר 5.11); כיוון 'דף קרדיטים' (אושר 5.11): בלי תיקיות לפי תחום (התחומים יגדלו), בהדר ערימת דפי פרויקט, ניסוח קליל ולא 'AI'; תפקיד בעמוד פרויקט = כרטיס מקווקו עם חריצים; כל פרויקט דף נייר מנוקב ממורכז, תפקיד = שורת קרדיט עם נקודות מובילות וכיסא (רכיב RoleCredit); הסינון המקורי נשמר; בלי כרטיסי SaaS, צ'יפים עודפים ומחרוזות עם נקודה אמצעית; כלל: צבע הכפתור לא ממלא שטחים גדולים - להדר יש טוקן bg/hero; צבע הנגיעה לקישוט בלבד. אדום+זעפרן וטורקיז+פודרה נדחו; שם ומותג טרם הוכרעו - השתמש בטוקנים ולא בערכים קשיחים. הימנע מקרם+טרקוטה, כרטיסי SaaS זהים, גרדיאנטים וצללים. רספונסיביות (responsive-guard): כל מסך בשלושה פריימים (390/768/1280), Auto Layout עם FILL, מטרות לחיצה 44px, ובדיקה בצילום."
)


def main() -> int:
    try:
        data = json.load(sys.stdin)
        code = str((data.get("tool_input") or {}).get("code", ""))
        if not any(h in code for h in MUTATING_HINTS):
            return 0
        out = json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": REMINDER,
            }
        }, ensure_ascii=True)  # ASCII-escaped: safe on any Windows console codepage
        sys.stdout.write(out + "\n")
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
