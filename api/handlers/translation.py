import pymongo
from fastapi import APIRouter
from googletrans import Translator

from api.responses.detail import DetailResponse, StringResponse, ListResponse

from pymongo import MongoClient

# connect to mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client["translation-database"]
words = db.words

router = APIRouter(prefix="/api/v1/translation")


@router.get("/", response_model=StringResponse)
def translate_word():
    """
    This is demo translation endpoint
    """
    translator = Translator()

    translation = translator.translate("Bonjour", dest="en")

    return StringResponse(message=translation.text)


@router.get("/translate/{word}", response_model=DetailResponse)
async def get_translation_details(word: str, defs: bool | None, trans: bool | None):
    """
    This is word details translation endpoint
    """

    # check if the word is in db
    found = words.find_one({"word": word})
    if not found:
        # translate and add to db if word not in db
        translator = Translator()
        translation = translator.translate(word, dest="en")
        text = translation.text
        definitions = translation.extra_data["definitions"]
        possible_translations = translation.extra_data["possible-translations"]
        words.insert_one(
            {
                "word": word,
                "text": text,
                "possible_translations": possible_translations,
                "definitions": definitions,
            }
        )
    else:
        # get translation from db if there

        text = found["text"]
        possible_translations = found["possible_translations"]
        definitions = found["definitions"]

    # formatting response
    ctx = {"word": word, "text": text}

    if defs:
        ctx["definitions"] = definitions

    if trans:
        ctx["possible_translations"] = possible_translations

    return DetailResponse(message=ctx)


@router.get("/list", response_model=ListResponse)
async def get_words_list(
        defs: bool | None,
        trans: bool | None,
        sorting: bool | None,
        filtering: str = '',
        skip: int = 0,
        limit: int = 10,
):
    """
    This is the list of  translations endpoint
    """
    results = []

    # find all translations
    found_words = words.find().skip(skip).limit(limit)
    if sorting:
        print("sorted")
        found_words = found_words.sort("word", pymongo.ASCENDING)

    # rewrap translations depending on parameters
    for found in found_words:
        item = {}
        word = found["word"]
        item["word"] = word
        text = found["text"]
        item["text"] = text
        if trans:
            possible_translations = found["possible_translations"]
            item["possible_translations"] = possible_translations
        if defs:
            definitions = found["definitions"]
            item["definitions"] = definitions
        if filtering:
            if filtering in word:
                results.append(item)
        if not filtering:
            results.append(item)

    return ListResponse(message=results)


@router.get("/delete/{word}", response_model=StringResponse)
async def delete_word(
        word: str
):
    """
    This is delete endpoint
    """
    words.delete_one({'word': word})

    return StringResponse(message='Deleted {}'.format(word))
