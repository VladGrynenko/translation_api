from fastapi import APIRouter
from googletrans import Translator

from api.responses.detail import DetailResponse

router = APIRouter(prefix="/api/v1/translation")


@router.get("/", response_model=DetailResponse)
def translate_word():
    """
    This is demo translation endpoint
    """
    translator = Translator()
    translation = translator.translate(
        "Der Himmel ist blau und ich mag Bananen", dest="en"
    )
    return DetailResponse(message=translation.text)
