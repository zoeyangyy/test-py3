#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Time        : 2017/10/4 下午4:12
# @Author      : Zoe
# @File        : test2.py
# @Description :

import nltk
from nltk.corpus import brown
import math

def test1_post():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]

    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains(%s)' % word.lower()] = True
        return features

    featuresets = [(dialogue_act_features(post.text), post.get('class')) for
                   post in posts]

    size = int(len(featuresets)*0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))


def test2_tre():
    def rte_features(rtepair):
        extractor = nltk.RTEFeatureExtractor(rtepair)
        features = {}
        features['word_overlap'] = len(extractor.overlap('word'))
        features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
        features['ne_overlap'] = len(extractor.overlap('ne'))
        features['ne_hyp_extra'] = len(extractor.hyp_extra('ne'))
        return features
    rtepair = nltk.corpus.rte.pairs(['rte2_dev.xml'])[33]
    extractor = nltk.RTEFeatureExtractor(rtepair)
    print(extractor.text_words)
    print(extractor.hyp_words)
    print(extractor.overlap('word'))
    print(extractor.overlap('ne'))
    print(extractor.hyp_extra('word'))


def test3():
    def tag_list(tagged_sents):
        return [tag for sent in tagged_sents for (word,tag) in sent]

    def apply_tagger(tagger, corpus):
        return [tagger.tag(nltk.tag.untag(sent)) for sent in corpus]

    gold = tag_list(brown.tagged_sents(categories='editorial'))
    test = tag_list(apply_tagger(t2, brown.tagged_sents(categories='editorial')))
    cm = nltk.ConfusionMatrix(gold, test)
    print(cm.pp(sort_by_count=True, show_precents=True, truncate=9))


def test4_entro():
    def entropy(labels):
        freqdist = nltk.FreqDist(labels)
        probs = [freqdist.freq(l) for l in freqdist]
        return -sum(p*math.log(p,2) for p in probs)

    print(entropy(['1','2']))

test4_entro()