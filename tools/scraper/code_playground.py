import json
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize
import string

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# TODO: remove later!


def normalize_text(paragraph):
    stopwords = set(nltk.corpus.stopwords.words('english'))

    paragraph = """
            Lectures focus on introduction and explanation of key concepts and techniques.
            Tutorial/lab sessions provide students with opportunities to apply the theories and
            techniques in selected software engineering scenarios. Assignments, in-class
            exercises/quizzes, and the examination will be used to assess the students’
            understanding of the learned knowledge. The project requires the students to work
            in groups and apply the theories and techniques to solve problems in the development
            of serious software systems. Course's object.
            """

    slash_regex = re.compile("/")

    # punctuation_regex = re.compile("[^\w\s]")

    paragraph = slash_regex.sub(" ", paragraph)

    lemmatizer = WordNetLemmatizer()

    # Define function to lemmatize each word with its POS tag

    # POS_TAGGER_FUNCTION : TYPE 1

    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    original_words = word_tokenize(paragraph.lower())

    cleaned_words = []

    for word in original_words:
        if word not in stopwords and word not in string.punctuation and len(word) > 2:
            cleaned_words.append(word)
        else:
            continue

    # tokenize the sentence and find the POS tag for each token
    pos_tagged = nltk.pos_tag(cleaned_words)

    # print(pos_tagged)
    # # >[('the', 'DT'), ('cat', 'NN'), ('is', 'VBZ'), ('sitting', 'VBG'), ('with', 'IN'),
    # # ('the', 'DT'), ('bats', 'NNS'), ('on', 'IN'), ('the', 'DT'), ('striped', 'JJ'),
    # # ('mat', 'NN'), ('under', 'IN'), ('many', 'JJ'), ('flying', 'VBG'), ('geese', 'JJ')]

    # As you may have noticed, the above pos tags are a little confusing.

    # we use our own pos_tagger function to make things simpler to understand.
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
    # print(wordnet_tagged)
    # # >[('the', None), ('cat', 'n'), ('is', 'v'), ('sitting', 'v'), ('with', None),
    # # ('the', None), ('bats', 'n'), ('on', None), ('the', None), ('striped', 'a'),
    # # ('mat', 'n'), ('under', None), ('many', 'a'), ('flying', 'v'), ('geese', 'a')]

    lemmatized_paragraph = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_paragraph.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_paragraph.append(lemmatizer.lemmatize(word, tag))
    lemmatized_paragraph = " ".join(lemmatized_paragraph)

    # print(lemmatized_paragraph)

    print("sentences as a JSON file:\n{}".format(
        json.dumps(lemmatized_paragraph)))
