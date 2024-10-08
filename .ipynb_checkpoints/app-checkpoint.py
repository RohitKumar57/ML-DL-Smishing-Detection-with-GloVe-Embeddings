import streamlit as st
import pickle
import tensorflow as tf
from nltk.corpus import stopwords
import nltk
import string
from nltk.stem.porter import PorterStemmer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the TF-IDF vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))

# Load the model architecture
with open('model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

# Reconstruct the model
model = tf.keras.models.model_from_json(loaded_model_json)

# Load the model weights
model.load_weights('model_weights.weights.h5')

# Function to preprocess text
def transform_text(text):
    ps = PorterStemmer()
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

# Streamlit app
def main():
    st.title('Email Spam Classifier')
    input_sms = st.text_input('Enter the Message ')

    if st.button('Click to Predict'):
        transform_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transform_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.header("Spam")
        else:
            st.header('Not Spam')

if __name__ == '__main__':
    main()
