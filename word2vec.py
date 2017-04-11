# encoding=utf-8
import numpy
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def create_model():
    # inp为输入语料
    inp = './jieba-cut.txt'
    # outp1 为输出模型
    outp1 = './text200.model'
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=20)
    model.save(outp1)


def model_usage():
    # 导入模型
    model = gensim.models.Word2Vec.load("./text200.model")
    # print(model['锌'])
    result = model.most_similar('糖尿病')  # 求余弦

    word =[]
    for each in result:
        print(each[0], each[1])
        word.append(each[0])

    print(word)

    # 两个词语similar的求法
    # A = model['高血压']
    # B = model['冠心病']
    # num = float(A.dot(B))  # 若为行向量则 A * B.T
    # denom = numpy.linalg.norm(A) * numpy.linalg.norm(B)
    # cos = num / denom  # 余弦值
    # print(cos)

    # model.most_similar(positive=['woman', 'king'], negative=['man'])
    # sim1 = model.similarity('贫血', '细胞')
    # print(sim1)

    # 找出最不相关的词
    # list = ['冠心病', '高血压', '糖尿病', '今天']
    # print(model.doesnt_match(list))


model_usage()
# create_model()
