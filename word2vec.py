# encoding=utf-8
import numpy
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


def create_model():
    # inp为输入语料
    inp = '/Users/zoe/Documents/remotefile2/disease-cut.txt'
    # outp1 为输出模型
    outp1 = '/Users/zoe/Documents/remotefile2/text200.model'
    # outp2为原始c版本word2vec的vector格式的模型
    # outp2 = '/Users/zoe/Documents/remotefile2/text.vector'
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=20)
    model.save(outp1)
    # model.wv.save_word2vec_format(outp2, binary=False)


def model_usage():
    # 导入模型
    model = gensim.models.Word2Vec.load("/Users/zoe/Documents/remotefile2/text200.model")
    # print(model['锌'])
    result = model.most_similar('高血压')  # 就是求了余弦
    for each in result:
        print(each[0], each[1])

    A = model['高血压']
    B = model['冠心病']
    num = float(A.dot(B))  # 若为行向量则 A * B.T
    denom = numpy.linalg.norm(A) * numpy.linalg.norm(B)
    cos = num / denom  # 余弦值
    print(cos)

    # model.most_similar(positive=['woman', 'king'], negative=['man'])
    # sim1 = model.similarity('贫血', '细胞')
    #  print(sim1)
    # list = [u'纽约', u'北京', u'上海', u'西瓜']
    # print(model.doesnt_match(list))

    # model = gensim.models.Word2Vec.load("/Users/zoe/Documents/remotefile2/text.model")
    # # print(model['锌'])
    # result = model.most_similar('贫血')
    # for each in result:
    #     print(each[0], each[1])
    # # model.most_similar(positive=['woman', 'king'], negative=['man'])
    # sim1 = model.similarity('贫血', '细胞')
    # print(sim1)

model_usage()
