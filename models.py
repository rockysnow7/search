import keras
import os

from keras.layers import Input, Dense
from keras import Model


MAX_TOKEN_LEN = 100
MAX_CHAR_ORD = 1023

WORD_AE_INPUT_SIZE = 500


def load_word_ae() -> Model:
    if "word_ae" in os.listdir():
        word_ae = keras.models.load_model("word_ae")
        word_ae_encoder = Model(word_ae.layers[0], word_ae.layers[2])
    else:
        input_layer = Input(shape=(WORD_AE_INPUT_SIZE,))
        encoded = Dense(WORD_AE_INPUT_SIZE // 2, activation="relu")(input_layer)
        encoded = Dense(1, activation="relu")(encoded)
        decoded = Dense(WORD_AE_INPUT_SIZE // 2, activation="sigmoid")(encoded)
        decoded = Dense(WORD_AE_INPUT_SIZE, activation="sigmoid")(decoded)

        word_ae = Model(input_layer, decoded)
        word_ae_encoder = Model(input_layer, encoded)

        word_ae.compile(optimizer="adam", loss="binary_crossentropy")

    return word_ae, word_ae_encoder

def load_text_ae() -> Model:
    if "text_ae" in os.listdir():
        text_ae = keras.models.load_model("text_ae")
        text_ae_encoder = Model(text_ae.layers[0], text_ae.layers[2])
    else:
        input_layer = Input(shape=(5000,))
        encoded = Dense(2500, activation="relu")(input_layer)
        encoded = Dense(100, activation="relu")(encoded)
        decoded = Dense(2500, activation="sigmoid")(encoded)
        decoded = Dense(5000, activation="sigmoid")(decoded)

        text_ae = Model(input_layer, decoded)
        text_ae_encoder = Model(input_layer, encoded)

        text_ae.compile(optimizer="adam", loss="binary_crossentropy")

    return text_ae, text_ae_encoder
