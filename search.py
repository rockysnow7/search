import requests
import keras
import os

from typing import List
from bs4 import BeautifulSoup

from keras.layers import Input, Dense
from keras import Model


def index_url(url: str) -> List[float]:
	# get html and format it nicely
	html = requests.get(url).text
	soup = BeautifulSoup(html, features="html.parser")
	for script in soup(["script", "style"]):
		script.extract()

	text = soup.body.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = "\n".join(chunk for chunk in chunks if chunk)

	# train the text autoencoder
	if "text_ae" in os.listdir():
		text_ae = keras.models.load_model("text_ae")
		text_ae_encoder = Model(text_ae.layers[0], text_ae.layers[2])
	else:
		encoded_dim = 100
		input_layer = Input(shape=(5000,))
		encoded = Dense(2500, activation="relu")(input_layer)
		encoded = Dense(encoded_dim, activation="relu")(encoded)
		decoded = Dense(2500, activation="sigmoid")(encoded)
		decoded = Dense(5000, activation="sigmoid")(decoded)

		text_ae = Model(input_layer, decoded)
		text_ae_encoder = Model(input_layer, encoded)

		text_ae.compile(optimizer="adam", loss="binary_crossentropy")