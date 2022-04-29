import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.translate.bleu_score import sentence_bleu
cur_path = os.path.dirname(os.path.abspath(__file__))


def calculate_bleu_score(reference_text, candidate_text):
    reference = [
        str(x).split() for x in reference_text
    ]

    candidate = str(candidate_text).split()
    score = sentence_bleu(reference, candidate, weights=(0.9, 0.1))
    return score


def load_t5_model(language):
    """
    load tokenizer and model from local path.
    """
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(cur_path, "models", language))
    model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(cur_path, "models", language))
    return tokenizer, model


# load model(Hindi and Urdu)
TR_MODEL = {
    "hindi": load_t5_model("hindi"),
    "urdu": load_t5_model("urdu")
}
print("model successfully loaded.")


def get_translation(text, lang="hindi"):
    """
    translate 'text' from Indian language to English.
    Support languages: Hindi, Urdu
    """
    one_line_text = str(text).replace("\n", " ")
    stripped_text = one_line_text.strip()
    if stripped_text == "":
        return ""

    tokenizer, model = TR_MODEL[lang]

    inputs = tokenizer.encode(
        stripped_text, return_tensors="pt", padding=True, max_length=512, truncation=True)

    outputs = model.generate(
        inputs, max_length=128, num_beams=None, early_stopping=True)

    translate_list = []
    for output in outputs:
        translated = tokenizer.decode(output).replace('<pad>',"").strip().lower()
        translate_list.append(translated)
    
    score = calculate_bleu_score(translate_list, translate_list[0])
    print("source text: {}\ntranslation: {}\nscore: {}".format(text, translated, score))

    return translated, score

