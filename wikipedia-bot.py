# Required modules and libraries

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters
import telegram
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
import requests
import wikipediaapi
import re
from uuid import uuid4

# Variables used
wiki_wiki = wikipediaapi.Wikipedia('fa')
message = "What do you wanna search for?"
aboutmsg = "Searching Wikipedia has never been easier! Just send a topic."


# Private chat with bot
# uses en wikipedia for english and fa wikipedia for persian inputs
def echo(update, context):
    output = re.search(r'^[a-zA-Z]+\Z', update.message.text)
    if output:
        wiki_wiki = wikipediaapi.Wikipedia('en')
    else:
        wiki_wiki = wikipediaapi.Wikipedia('fa')

    page_py = wiki_wiki.page(update.message.text)
    if page_py.exists():
        wikimsg = (page_py.fullurl)
        update.message.reply_text(wikimsg)
    else:
        update.message.reply_text("Your search querry had no results.")

# In-line mode
def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    output = re.search(r'^[a-zA-Z]+\Z', query)
    if output:
        wiki_wiki = wikipediaapi.Wikipedia('en')
    else:
        wiki_wiki = wikipediaapi.Wikipedia('fa')

    page_py = wiki_wiki.page(query)
    if page_py.exists():
        wikimsg = (page_py.fullurl)
        pagetitle= page_py.title
        results = [InlineQueryResultArticle(
            description="Searching for" + " " + query+ " " + "in Wikipedia",
            id=uuid4(),
            title=pagetitle,
            input_message_content=InputTextMessageContent(
                    message_text=wikimsg))
            ]

        update.inline_query.answer(results)
    else:
        results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="No results",
            input_message_content=InputTextMessageContent(query)
            )]

        update.inline_query.answer(results)


def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,text =message)
def about(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,text =aboutmsg)



updater = Updater(token = 'TOKEN', use_context=True)
bot = telegram.Bot(token='TOKEN')
dispatcher = updater.dispatcher

def main():
    start_handler = CommandHandler('start',start)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler('about',about))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()


