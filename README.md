
# Translation Web Service for Indian to English

## How to run this service

You should have python3.7(or later) and pip installed on your machine.
```shell
pip3 install -r requirements.txt
```
If _torch_ library is not working correctly, you can install it from  their [website](https://pytorch.org/get-started/locally/).

```shell
pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
```

## How it works

Translation is the task of converting text from one language to another.

Translation converts a sequence of text from one language to another. It is one of several tasks you can formulate as a sequence-to-sequence problem, a powerful framework that extends to vision and audio tasks.

This is a sequence-to-sequence task, which means it’s a problem that can be formulated as going from one sequence to another. In that sense the problem is pretty close to summarization, and you could adapt what we will see here to other sequence-to-sequence problems such as:

- Style transfer: Creating a model that translates texts written in a certain style to another (e.g., formal to casual or Shakespearean English to modern English)
- Generative question answering: Creating a model that generates answers to questions, given a context


This model is trained on OPUS dataset. This open parallel is the collection of translated texts from the web. 

It also includes translations of Wikipedia, WikiSource, WikiBooks, WikiNews and WikiQuote web pages. This [GitHub page](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/Backtranslations.md) will provide the link to download the source and the target texts obtained from wiki web pages. 

Here is the code snippet that is needed to convert the text from Hindi to English.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

hin_snippet = "हम इन्फोवेब हैं। यह एक प्राकृतिक भाषा अनुवाद परियोजना है"
inputs = tokenizer.encode(
    hin_snippet, return_tensors="pt",padding=True,max_length=512,truncation=True)

outputs = model.generate(
    inputs, max_length=128, num_beams=None, early_stopping=True)

translated = tokenizer.decode(outputs[0]).replace('<pad>',"").strip().lower()
print(translated)
# We are Infoweb. This is a natural language translation project
```

source-language: [Hindi, Urdu, Telugu, Tamil, Odia]

target-language: English


# File structure

1) app.py
```
Using flask library, we're running service on port 1234 and also rendering html page.
It's implemented in @app.route('/') function.
```
2) routes.py
```
In this script, we define endpoint for the web service.
For example, you can request some processing from frontrend(javascript code) to this endpoint '/get_message').
This endpoint function was defined in IndicTranslator class in translator.py file.
```
3) trans_util.py
```
This is translation utility.
We used transformer model for text translation, and used BLEU score of NLTK(Natural Language ToolKit) library to get score value.
```
4) translator.py
```
This script is for request processing from frontend.
It receives request in POST method and calls translator function in trans_util.py file.
And returns the data as JSON format.
```
5) models folder
'''
It includes translation model for hindi and urdu language for now. You can see the document details in above (How it works) for model works.
'''

In registerUi.js file, you can change the endpoint, and change/add parameters here.
