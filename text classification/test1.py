#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/2 下午4:56
# @Author      : Zoe
# @File        : test1.py
# @Description :


import nltk
from nltk.corpus import names
from nltk.corpus import movie_reviews
from nltk.corpus import brown
from nltk.classify import apply_features
import random


def gender_features(word):
    return {'last_letter': word[-1], 'suffix2': word[-2:]}
# other features
# 'first_letter:': word[0], 'lens': len(word)


def test1():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')]+
                     [(name, 'female') for name in names.words('female.txt')])

    # print(labeled_names)
    random.shuffle(labeled_names)
    featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
    # print(len(featuresets))
    train_set, test_set = featuresets[500:], featuresets[:500]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    # train_set = apply_features(gender_features, labeled_names[500:])

    # print(classifier.classify(gender_features('Neo')))
    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(5))


def test2():
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
                     [(name, 'female') for name in names.words('female.txt')])

    random.shuffle(labeled_names)

    train_names = labeled_names[1500:]
    devtest_names = labeled_names[500:1500]
    test_names = labeled_names[:500]

    train_set = [(gender_features(n), gender) for (n, gender) in train_names]
    devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
    test_set = [(gender_features(n), gender) for (n, gender) in test_names]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, devtest_set))

    errors = []
    for (name, tag) in devtest_names:
        guess = classifier.classify(gender_features(name))
        if guess != tag:
            errors.append((tag, guess, name))
    for (tag, guess, name) in sorted(errors):
        print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))


def test3_movie():
    documents = [(list(movie_reviews.words(fileid)), category) for
                 category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)

    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = list(all_words)[:2000]

    def document_features(document):
        documents_words = set(document)
        features = {}
        for word in word_features:
            features['contain({})'.format(word)] = (word in documents_words)
        return features

    def bag_of_words(words):
        return dict([word, True] for word in words)

    # print(document_features(movie_reviews.words('pos/cv957_8737.txt')))
    featuresets = [(document_features(d),c) for (d,c) in documents]
    train_set, test_set = featuresets[100:],featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(5))

# test3_movie()

def test4_brown():
    suffix_fdist = nltk.FreqDist()
    for word in brown.words():
        word = word.lower()
        suffix_fdist[word[-1:]] += 1
        suffix_fdist[word[-2:]] += 1
        suffix_fdist[word[-3:]] += 1

    common_suffixes = [suffix for (suffix, count) in suffix_fdist.most_common(100)]
    print(common_suffixes)

    def pos_features(word):
        features = {}
        for suffix in common_suffixes:
            features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
        return features

    tagged_words = brown.tagged_words(categories='news')
    featuresets = [(pos_features(n), g) for (n,g) in tagged_words]
    print(featuresets[0])
    size = int(len(featuresets)*0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]

    classifier = nltk.DecisionTreeClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    classifier.classify(pos_features('cats'))
    print(classifier.pseudocode(depth=4))
    # 0.6270512182993535


def test5_brown():
    def pos_features(sentence, i):
        features = {"suffix(1)": sentence[i][-1:],
                    "suffix(2)": sentence[i][-2:],
                    "suffix(3)": sentence[i][-3:]}
        if i == 0:
            features["prev-word"] = "<START>"
        else:
            features["prev-word"] = sentence[i - 1]
        print(features)
        return features

    pos_features(brown.sents()[0],8)
    tagged_sents = brown.tagged_sents(categories='news')
    featuresets = []
    for tagged_sent in tagged_sents:
        untagged_sent = nltk.tag.untag(tagged_sent)
        for i, (word, tag) in enumerate(tagged_sent):
            featuresets.append((pos_features(untagged_sent,i), tag))
    size = int(len(featuresets)*0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    nltk.classify.accuracy(classifier, test_set)


def test6_brown():
    def pos_features(sentence, i, history):
        features = {"suffix(1)": sentence[i][-1:],
                    "suffix(2)": sentence[i][-2:],
                    "suffix(3)": sentence[i][-3:]}
        if i == 0:
            features["prev-word"] = "<START>"
            features["prev-tag"] = "<START>"
        else:
            features["prev-word"] = sentence[i - 1]
            features["prev-tag"] = history[i - 1]
        return features

    class ConsecutivePosTagger(nltk.TaggerI):
        def __init__(self, train_sents):
            train_set = []
            for tagged_sent in train_sents:
                untagged_sent = nltk.tag.untag(tagged_sent)
                history = []
                for i, (word, tag) in enumerate(tagged_sent):
                    featureset = pos_features(untagged_sent, i, history)
                    train_set.append((featureset, tag))
                    history.append(tag)
            self.classifier = nltk.NaiveBayesClassifier.train(train_set)

        def tag(self, sentence):
            history = []
            for i, word in enumerate(sentence):
                featureset = pos_features(sentence, i, history)
                tag = self.classifier.classify(featureset)
                history.append(tag)
            return zip(sentence, history)

    tagged_sents = brown.tagged_sents(categories='news')
    size = int(len(tagged_sents) * 0.1)
    train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
    tagger = ConsecutivePosTagger(train_sents)
    print(tagger.evaluate(test_sents))
    # 0.7980528511821975

test6_brown()