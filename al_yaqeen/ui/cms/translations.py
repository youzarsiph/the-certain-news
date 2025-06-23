"""Custom MachineTranslator to integrate HuggingFace Hub translations"""

from huggingface_hub import InferenceClient
from wagtail_localize.machine_translators.base import BaseMachineTranslator
from wagtail_localize.strings import StringValue


class HuggingFaceTranslator(BaseMachineTranslator):
    """HuggingFace Translator"""

    client = InferenceClient()
    display_name = "HuggingFace"

    def translate(self, source_locale, target_locale, strings):
        """Translate articles from source_locale to target_locale"""

        return {
            string: StringValue.from_plaintext(
                self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Can you translate the following text from {source_locale.language_code} to {target_locale.language_code}:\n{string.render_text()}",
                        }
                    ],
                    model="mistralai/Mistral-7B-Instruct-v0.3",
                )
                .choices[0]
                .message.content
            )
            for string in strings
        }

    def can_translate(self, source_locale, target_locale):
        """Check if it is possible to translate"""

        return source_locale.language_code != target_locale.language_code
