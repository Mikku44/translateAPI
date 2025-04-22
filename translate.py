from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_mapping = {
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "en-th": "facebook/m2m100_418M",
    "th-en": "Helsinki-NLP/opus-mt-th-en",
    "th-fr": "Helsinki-NLP/opus-mt-th-fr",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
    "en-de": "Helsinki-NLP/opus-mt-en-de",
    "en-ja": "Helsinki-NLP/opus-mt-en-jap",
    "en-zh": "Helsinki-NLP/opus-mt-en-zh",
    "en-it": "Helsinki-NLP/opus-mt-en-it",
    "en-vi": "Helsinki-NLP/opus-mt-en-vi",
    "en-id": "Helsinki-NLP/opus-mt-en-id",
    "en-ru": "Helsinki-NLP/opus-mt-en-ru",
    "en-ar": "Helsinki-NLP/opus-mt-en-ar",
}


def translate_text(source_lang: str, target_lang: str, text: str):
    """
    Translate text between supported languages.
    
    Args:
        source_lang: Source language code (e.g., 'en')
        target_lang: Target language code (e.g., 'es')
        text: Text to translate
    """
    lang_pair = f"{source_lang}-{target_lang}"
    
    if lang_pair not in model_mapping:
        raise ValueError(f"Unsupported language pair: {lang_pair}. Available pairs: {list(model_mapping.keys())}")
    
    try:
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_mapping[lang_pair])
        model = AutoModelForSeq2SeqLM.from_pretrained(model_mapping[lang_pair])
        
        
        # Tokenize and translate
        inputs = tokenizer(text, return_tensors="pt")
        if(model_mapping[lang_pair] == "facebook/m2m100_418M"):
            outputs = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.get_lang_id("th")
            )
        else :
            outputs = model.generate(**inputs)
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")




# Example Usage
if __name__ == "__main__":
    # English → Spanish
    print(translate_text("en", "es", "Hello, world!"))  # Output: ¡Hola, mundo!
    
    # English → Thai
    # print(translate_text("en", "th", "Good morning"))    # Output: สวัสดีตอนเช้า
    
    # Spanish → English
    print(translate_text("es", "en", "¿Cómo estás?"))    # Output: How are you?