"""HuggingFace Machine translator"""

from typing import Any, Dict, List
import logging

from django.conf import settings
from huggingface_hub import InferenceClient
from wagtail.models import Locale
from wagtail_localize.strings import StringValue
from wagtail_localize.machine_translators.base import BaseMachineTranslator


logger = logging.getLogger(__name__)


# Create your translators here.
class HuggingFaceTranslator(BaseMachineTranslator):
    """Machine translator to translate pages using HuggingFace Hub"""

    display_name = "HuggingFace"

    # Settings
    HF_TRANSLATION_MODEL = getattr(
        settings,
        "HF_TRANSLATION_MODEL",
        "meta-llama/Meta-Llama-3-8B-Instruct",
    )
    SYSTEM_MESSAGE = """You are a professional multi-lingual editor and translator.
    Translate the provided segments into the requested target language EXACTLY as specified.
    - Use Modern Standard Arabic for Arabic targets, suitable for news publishing.
    - Preserve meaning, clarity, and concise headline tone when applicable.
    - Do NOT add diacritics. Respect sentence punctuation.
    - Do NOT change numbers, URLs, HTML attributes, or IDs.
    """

    client = InferenceClient(model=HF_TRANSLATION_MODEL)

    def trans(self, text: str, src: str, tgt: str) -> str:
        """
        Perform AI translation

        Args:
            text (str): Translated text.
            src (str): Source Locale language code.
            tgt (str): Target Locale language code.

        Returns:
            str: Translation output.
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.SYSTEM_MESSAGE},
                    {
                        "role": "user",
                        "content": f"Translate the following text from {src} to {tgt}:\n {text}",
                    },
                ],
            )

            return str(response.choices[0].message.content)

        except Exception as e:
            logger.error("Translation failed: %s", e, exc_info=True)

            return "Failed to translate. Please try again later."

    def translate(
        self,
        source_locale: Locale,
        target_locale: Locale,
        strings: List[StringValue],
    ) -> Dict[Any, StringValue]:
        """
        Perform translation using HuggingFace

        Args:
            source_locale (Locale): Source locale
            target_locale (Locale): Target Locale
            strings (List): Translated strings

        Returns:
            Dict: Translation output
        """

        return {
            string: StringValue.from_translated_html(
                self.trans(
                    string.get_translatable_html(),
                    source_locale.language_code,
                    target_locale.language_code,
                )
            )
            for string in strings
        }

    def can_translate(self, source_locale, target_locale) -> bool:
        """Check if translations is possible.

        Args:
            source_locale (Locale): Source Locale.
            target_locale (Locale): Target Locale.

        Returns:
            bool: Boolean indicating if it translation is possible.
        """

        return source_locale.language_code != target_locale.language_code
