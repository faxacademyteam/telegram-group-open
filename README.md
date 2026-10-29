# Telegram Group Auto Lock/Unlock + Pin for 1 Minute

## Daily schedule (Bangladesh time, UTC+6)
- 10:00 AM: unlock the group, send the OPEN notice, pin it with pin notification enabled, wait 60 seconds, then unpin that message.
- 6:00 PM: lock the group, send the OFF notice, pin it with pin notification enabled, wait 60 seconds, then unpin that message.

## Setup
1. Create a private GitHub repository.
2. Upload `bot.py`, `README.md`, and `.github/workflows/group-schedule.yml`.
3. Go to Settings → Secrets and variables → Actions and add:
   - `BOT_TOKEN`: Telegram bot token
   - `CHAT_ID`: target group ID
4. The bot must be an administrator with permission to manage chat permissions and pin messages.
5. Open Actions → Telegram Group Auto Lock Unlock → Run workflow and test `unlock` and `lock`.

## Behavior
- The status message is sent only after the permissions update succeeds.
- The bot pins the newly sent notice with `disable_notification=false`, requesting a normal pin notification.
- The script waits about 60 seconds, then unpins that exact message using Telegram's `unpinChatMessage` API.
- The message itself remains in the chat; it is not deleted.
- The unpin action removes the pin from the specified message. Depending on Telegram's group pin behavior, any older pinned messages are not intentionally changed.
- Telegram cannot guarantee every member's device receives a notification.
- GitHub Actions may start late; the one-minute timer begins after the job runs and the message is pinned, not exactly at the scheduled clock time.
- The workflow runner remains active for the extra minute; this is normally a small amount of GitHub Actions usage.
