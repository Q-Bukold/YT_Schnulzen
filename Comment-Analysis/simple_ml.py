from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


#Wir können die Methode "CountVectorizer" aus scikit-learn verwenden. 
#Sie überführt die Tokens eines Textdokuents in eine Matrix mit Wortzählungen.

def get_keywords_from_string(doc, word_range=1, top_n=20, stop_words = "english"):
    n_gram_range = (1, word_range)

    # Extract candidate words/phrases
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
    candidates = count.get_feature_names_out()

    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)

    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]

    return keywords