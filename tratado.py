import re
import unicodedata
import inflect
from spacy.lang.es.stop_words import STOP_WORDS
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

ps = SnowballStemmer('spanish')
p = inflect.engine()

# Función para limpiar caracteres especiales y convertir a ASCII
def limpiar_ascii(text):
    return [unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') for word in text]

# Función para convertir a minúsculas
def limpiar_minusculas(text):
    return [word.lower() for word in text]

# Función para limpiar puntuación utilizando expresiones regulares
def limpiar_puntuacion(text):
    return [re.sub(r'[^\w\s]', '', word) for word in text if re.sub(r'[^\w\s]', '', word) != '']

# Función para cambiar números a texto
def limpiar_numeros(text):
    return [p.number_to_words(word) if word.isdigit() else word for word in text]

# Función para quitar stopwords
def remove_stopwords(text):
    return [word for word in text if word not in STOP_WORDS]

# Función para aplicar las funciones de limpieza
def procesar_texto(text):
    text = limpiar_ascii(text)
    text = limpiar_minusculas(text)
    text = limpiar_puntuacion(text)
    text = limpiar_numeros(text)
    return text

# Función para aplicar el stemmer de Snowball
def porter_stemmer_spanish(text):
    return [ps.stem(word) for word in text]

# Función para unir palabras
def join_words(words):
    return ' '.join(words)

# Función para procesar los datos
def process_data(text):
    return text.apply(porter_stemmer_spanish).apply(join_words)


def limpiar_texto(texto):
    tokenizado = word_tokenize(texto)
    procesado = procesar_texto(tokenizado)
    stemmizado = porter_stemmer_spanish(procesado)
    completado = join_words(stemmizado)
    return completado
