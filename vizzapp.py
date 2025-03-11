import os
import logging
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Firebase
cred = credentials.Certificate("vizzapp-serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load bot info from .env
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Command handlers
async def sentence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /frase command."""
    try:
        doc_ref = db.collection("sentencesCollection").get()
        sentences = []
        for doc in doc_ref:
            document_data = doc.to_dict()
            if "sentences" in document_data and isinstance(document_data["sentences"], list):
                sentences.extend(document_data["sentences"])

        if sentences:
            if context.args:
                try:
                    requested_index = int(context.args[0]) - 1
                    if 0 <= requested_index < len(sentences):
                        chosen_sentence = sentences[requested_index]
                        message = f"Frase #{requested_index + 1}: {chosen_sentence}"
                    else:
                        message = "Indice frase non valido."
                except ValueError:
                    message = "Input non valido. Fornire un numero."
            else:
                random_index = random.randint(0, len(sentences) - 1)
                chosen_sentence = sentences[random_index]
                message = f"Frase #{random_index + 1}: {chosen_sentence}"
        else:
            message = "Nessuna frase disponibile."
        await update.message.reply_text(message)
    except KeyError:
        await update.message.reply_text("Errore: alcuni dati nel database non sono formattati correttamente.")
    except Exception as e:
        print(f"Errore generico: {e}")
        await update.message.reply_text("Si è verificato un errore inaspettato.")

async def all_sentences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /tutte_frasi command."""
    try:
        doc_ref = db.collection("sentencesCollection").get()
        sentences = []
        for doc in doc_ref:
            document_data = doc.to_dict()
            if "sentences" in document_data and isinstance(document_data["sentences"], list):
                sentences.extend(document_data["sentences"])

        if sentences:
            for i in range(0, len(sentences), 50):
                chunk = sentences[i:i + 50]
                message = ""
                for index, sentence in enumerate(chunk):
                    message += f"{i + index + 1}. {sentence}\n"
                await update.message.reply_text(message)
        else:
            await update.message.reply_text("Nessuna frase disponibile.")
    except Exception as e:
        print(f"Errore generico: {e}")
        await update.message.reply_text("Si è verificato un errore inaspettato.")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for logging errors."""
    logger.error(f'Update "{update}" caused error "{context.error}"')

# Create the Application instance
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("frase", sentence))
app.add_handler(CommandHandler("tutte_frasi", all_sentences))

# Errors
app.add_error_handler(error)

# Polling
app.run_polling()