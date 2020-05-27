from spellchecker import SpellChecker
import pickle

spell = SpellChecker()
target_words = pickle.load(open('target_words_all.txt', 'rb'))
misspelled = spell.unknown(target_words)
spell.word_frequency.load_words(misspelled)

