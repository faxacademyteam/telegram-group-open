```python
import os
import json
import time
import urllib.request
import urllib.error

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

API = f"https://api.telegram.org/bot{TOKEN}/"


def call(method, payload):
    req = urllib.request.Request(
        API + method,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            exc.read().decode(errors="replace")
        ) from exc

    if not result.get("ok"):
        raise RuntimeError(
            f"Telegram API error in {method}: {result}"
        )

    return result["result"]


def notice(mode):
    # Only the Buy-Sell time line is quoted.
    time_quote = (
        "<blockquote>"
        "⏰ <b>Buy-Sell Time: 10:00 AM – 06:00 PM</b>"
        "</blockquote>\n\n"
    )

    if mode == "unlock":
        return (
            time_quote
            + "🟢 <b>গ্রুপ OPEN হয়েছে! 🏦</b>\n\n"
            + "আজ সকাল ১০টা থেকে ডলার Buy-Sell কার্যক্রম "
            "শুরু হয়েছে। এখন আপনারা ডলার কেনা-বেচা "
            "করতে পারবেন।\n"
            + "━━━━━━━━━━━━━━━━━━\n"
            + "🔴 <b>Group Auto OFF:</b> সন্ধ্যা ৬টায়।\n\n"
            + "🙏 <b>ধন্যবাদ | Thank You</b> 🤍"
        )

    return (
        time_quote
        + "🔴 <b>আজকের মতো গ্রুপ বন্ধ!</b> "
        + "আজ সন্ধ্যা ৬টায় গ্রুপ অটো OFF হয়েছে।\n"
        + "━━━━━━━━━━━━━━━━━━\n"
        + "🟢 <b>Tomorrow:</b> সকাল ১০টায় গ্রুপ আবার "
        + "অটো OPEN হবে।\n\n"
        + "🙏 <b>ধন্যবাদ | Thank You</b> 🤍"
    )


def send_pin_wait_unpin(text):
    # Send the notice using Telegram HTML formatting.
    message = call("sendMessage", {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })

    message_id = message["message_id"]

    print(f"Notice sent successfully. Message ID: {message_id}")

    # Pin the notice with notification enabled.
    call("pinChatMessage", {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "disable_notification": False,
    })

    print("Notice pinned with notification enabled.")

    # Keep it pinned for approximately 60 seconds.
    time.sleep(60)

    # Unpin the exact message sent by this workflow.
    call("unpinChatMessage", {
        "chat_id": CHAT_ID,
        "message_id": message_id,
    })

    print("Notice automatically unpinned after 60 seconds.")


def main():
    mode = os.environ.get("MODE", "").strip().lower()

    if mode not in ("lock", "unlock"):
        raise SystemExit(
            "Invalid MODE. Set MODE to 'lock' or 'unlock'."
        )

    allow = mode == "unlock"

    permissions = {
        key: allow
        for key in (
            "can_send_messages",
            "can_send_audios",
            "can_send_documents",
            "can_send_photos",
            "can_send_videos",
            "can_send_video_notes",
            "can_send_voice_notes",
            "can_send_polls",
            "can_send_other_messages",
            "can_add_web_page_previews",
        )
    }

    # Update group permissions before sending the notice.
    call("setChatPermissions", {
        "chat_id": CHAT_ID,
        "permissions": permissions,
        "use_independent_chat_permissions": True,
    })

    print(f"Group permissions updated: {mode.upper()}")

    # Send, pin, wait 60 seconds, then unpin.
    send_pin_wait_unpin(notice(mode))


if __name__ == "__main__":
    main()
```
