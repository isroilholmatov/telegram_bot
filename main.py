from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔥 BU YERGA O'ZINGIZNING TOKENINGIZNI QO'YING
TOKEN = "7058823314:AAEFuRC3e-xrIyc9kHO3lUjOQXhGYG1352E"

# 🔥 BU YERGA O'Z TELEGRAM ID-INGIZNI QO'YING (O'qituvchi)
TEACHER_ID = 2049918772

# ✅ /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    student_id = user.id
    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    # O'qituvchiga yangi o'quvchi haqida habar
    await context.bot.send_message(
        chat_id=TEACHER_ID,
        text=f"📢 Yangi o'quvchi start bosdi:\n👤 Ismi: {full_name}\n🆔 ID: `{student_id}`",
        parse_mode="Markdown"
    )

    # O'quvchiga javob
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n"
        "Uyga vazifani matn yoki rasm shaklida yuboring.\n"
        "Men tez orada javob qaytaraman."
    )

# ✅ Matnli xabarlarni qabul qilish
async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=TEACHER_ID,
        text=f"📩 {user.first_name} ({user.id}) yubordi:\n{text}"
    )

    await update.message.reply_text("✅ Xabaringiz qabul qilindi.")

# ✅ Rasm qabul qilish
async def photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=TEACHER_ID,
        photo=photo,
        caption=f"📷 {user.first_name} ({user.id}) rasm yubordi."
    )

    await update.message.reply_text("✅ Rasm qabul qilindi.")

# ✅ O'qituvchi javob berishi uchun
async def reply_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Masalan: /reply student_id matn"""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❗ Foydalanish: /reply student_id matn")
        return

    student_id = args[0]
    answer_text = " ".join(args[1:])
    await context.bot.send_message(chat_id=student_id, text=f"📢 O'qituvchi javobi:\n{answer_text}")
    await update.message.reply_text("✅ Javob yuborildi.")

# ✅ Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply_student))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
app.add_handler(MessageHandler(filters.PHOTO, photo_message))

print("✅ Bot ishga tushdi...")
app.run_polling()
