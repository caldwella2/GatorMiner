"""Where NLP modules should be in"""
from collections import Counter
import re
import string
from typing import List, Tuple
import spacy
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from . import markdown as md

PARSER = spacy.load("en_core_web_sm")


def normalize(data: str) -> str:
    """Remove numbers, single characters, to lowercase"""
    data = data.lower()
    normalized_data = re.sub(r"\b[a-zA-Z]\b|\b[0-9]+\b", "", data)
    normalized_data = "".join(c for c in normalized_data if c not in string.punctuation)
    return normalized_data


def tokenize(normalized_text: str) -> List[str]:
    """break down text into a list of lemmatized tokens"""
    tokens = PARSER(normalized_text)
    # lemmatize tokens
    tokens = [
        word.lemma_.strip()
        for word in tokens
        if word.lemma_ != "-PRON-" and word.is_stop is False
    ]
    tokens = [word for word in tokens if len(word) > 1]
    return tokens


def compute_frequency(token_lst: List[str], amount=50) -> List[Tuple[str, int]]:
    """Compute word frequency from a list of tokens"""
    word_freq = Counter(token_lst)
    return word_freq.most_common(amount)


def word_frequency(text: str, amount=50) -> List[Tuple[str, int]]:
    """A pipeline to normalize, tokenize, and
    find word frequency of raw text"""
    return compute_frequency(tokenize(normalize(text)), amount)


def dir_frequency(dirname: str, amount=50) -> List[Tuple[str, int]]:
    """A pipeline to normalize, tokenize, and
    find word frequency of a directory of raw input file"""
    file_list = md.get_file_names(dirname)
    doc_list = []
    for file in file_list:
        doc_list.append(md.read_file(file))
    return compute_frequency(tokenize(normalize(" ".join(doc_list))), amount)


def sentence_tokenize(input_text):
    """tokenize paragraph to a list of sentences"""
    sent_lst = []
    sent_pipe = PARSER.create_pipe("sentencizer")
    PARSER.add_pipe(sent_pipe)
    doc = PARSER(input_text)
    for sent in doc.sents:
        sent_lst.append(sent.text)
    return sent_lst


def part_of_speech(input_text):
    """part of speech tagging of sentence"""
    doc = PARSER(input_text)
    pos_lst = []
    for word in doc:
        pos_lst.append((word.text, word.pos_))
    return pos_lst


def compute_tfidf(data: List[str]) -> None:
    """Compute the TFIDF"""
    tfidf_vectorizer = TfidfVectorizer()
    # make data iterable for TFIDF
    tfs = tfidf_vectorizer.fit_transform([" ".join(data)])
    feature_names = tfidf_vectorizer.get_feature_names()
    for col in tfs.nonzero()[1]:
        print(feature_names[col], " - ", tfs[0, col])
    return tfs, tfidf_vectorizer


def compute_count_vectorize(data):
    """Compute the count vectorize matrix"""
    count_vectorizer = CountVectorizer()
    count = count_vectorizer.fit_transform(data)
    return count, count_vectorizer


def named_entity_recognization(input_text):
    """identifies important elements like places, people, organizations, and
    languages within an input string of text"""
    doc = PARSER(input_text)
    ent_lst = []
    for entity in doc.ents:
        print(entity, entity.label_)
        ent_lst.append((str(entity), entity.label_))
    # spacy.displacy.serve(doc, style="ent")
    # display in jupyter notebook
    # displacy.render(about_interest_doc, style='dep', jupyter=True)
    return ent_lst


def noun_phrase(input_text):
    """Extract noun phrases of the document in a list"""
    doc = PARSER(input_text)
    n_phrase_lst = []
    for chunk in doc.noun_chunks:
        n_phrase_lst.append(str(chunk))
    return n_phrase_lst
