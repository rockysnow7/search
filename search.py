import requests
import nltk
import cld3
import models

from typing import List
from bs4 import BeautifulSoup
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from keras.layers import Input, Dense
from keras import Model


def index_url(url: str) -> List[float]:
    # html -> just text -> tokens -> floats -> better floats
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.body.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    tokens = [token for token in nltk.word_tokenize(text) if len(token) <= models.MAX_TOKEN_LEN and not any(ord(char) > models.MAX_CHAR_ORD for char in token)]

    tokens_floats = [[(ord(char) + 1) / (models.MAX_CHAR_ORD + 1) for char in token] for token in tqdm(tokens)]
    tokens_floats = [floats + [0]*(models.WORD_AE_INPUT_SIZE - len(floats)) for floats in tqdm(tokens_floats)]
    x_train, x_test = train_test_split(tokens_floats, test_size=0.15)

    word_ae, word_ae_encoder = models.load_word_ae()
    word_ae.fit(
        x_train, x_train,
        epochs=50,
        batch_size=256,
        shuffle=True,
        validation_data=(x_test, x_test),
    )

    tokens_encoded = [word_ae_encoder.predict((token,))[0][0] for token in tqdm(tokens_floats)]
    print("tokens_encoded:", tokens_encoded)

    # train the text autoencoder
    text_ae, text_ae_encoder = models.load_text_ae()
