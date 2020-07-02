import jieba.posseg
from gensim import corpora, models, similarities
import scan
import numpy as np

'''
引用资料：https://blog.csdn.net/xc_zhou/article/details/80952460
        https://blog.csdn.net/xiexf189/article/details/79092629
        https://blog.csdn.net/Yellow_python/article/details/81021142
'''


def cutTheText(content):
    result = []
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']
    # 分词
    words = jieba.posseg.cut(content)
    for word, flag in words:
        if flag not in stop_flag:
            result.append(word)
    return result


def duplicateCheck(original_file, para):
    # 通过前面的方法得到文件夹中的内容
    all_content = scan.readFileContain(original_file, para)

    jieba.set_dictionary("./dict.txt")
    jieba.initialize()

    # 分词
    corpus = []
    for content in all_content:
        content_list = cutTheText(content)
        corpus.append(content_list)

    # 构建词料库dinctionary
    dictionary = corpora.Dictionary(corpus)
    print(dictionary)
    # 转化为bow模型
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    # 建立TF-IDF模型
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    res = []
    for query in corpus:
        # 过滤后的文本
        # 词袋的字典映射到向量空间
        query_bow = dictionary.doc2bow(query)

        # 建立LSI模型计算相似度
        lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=len(corpus))
        lsi_vector = lsi[tfidf_vectors]
        query_lsi = lsi[query_bow]
        index = similarities.MatrixSimilarity(lsi_vector)
        sims = index[query_lsi]
        res.append(list(sims))

    result = np.around(res, decimals=2)
    np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
    return result

'''
p1 = Parameter()
p1.setParameter(False, 7 ,0)
duplicateCheck("D:\网课\python\测试数据",p1)'''