from django.shortcuts import render
from django.http import *
from .models import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import math
import gensim
from gensim.models import word2vec
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import jieba
import codecs
import csv
import math
import json


def add(request):
    op = codecs.open('web/static/files/tengxun_qa.csv', 'r', encoding='utf_8_sig')
    csv_file = csv.reader(op)
    bank_ = Bank.objects.get(name='腾讯云题库')
    for i in csv_file:
        try:
            QuestionAnswer.objects.create(question=i[0], keywords=i[1], answer=i[2], url=i[3], bank=bank_)
        except Exception as e:
            pass
    # qa = QuestionAnswer.objects.all()
    # QuestionAnswer.objects.all().delete()
    qa = QuestionAnswer.objects.all()
    return render(request, 'index.html', {'qa': qa})

def delete(request):
    QuestionAnswer.objects.all().delete()
    qa = QuestionAnswer.objects.all()
    return render(request, 'index.html', {'qa': qa})

def index(request):
    return render(request, 'index.html')

def qustion_list(request):
    return render(request, 'question/list.html')

def question_list_filter(request, bid):
    pass


def question_create(request):
    return render(request, 'question/create.html')

def question_instance(request, qid):
    return render(request, 'question/instance.html', {'qid': qid})

def bank_list(request):
    return render(request, 'bank/list.html')

def bank_create(request):
    return render(request, 'bank/create.html')

def bank_instance(request, bid):
    return render(request, 'bank/instance.html', {'bid': bid})

def bank_question_list(request, bid):
    return render(request, 'bank/question.html', {'bid': bid})

def bank_question_add(request, bid):
    return render(request, 'bank/addquestion.html', {'bid': bid})


def question(request):
    return render(request, 'question.html')

def test(request):
    return render(request, 'question-client/test.html')

def bidui(quest, quest_):
    sents = []
    sents.append(quest_)
    sents.append(quest)
    vectorizer = TfidfVectorizer()
    wget = vectorizer.fit_transform(sents).toarray()
    # print("特征向量为：")
    # print(vectorizer.get_feature_names())
    va = wget[0]
    vb = wget[1]
    # print(va * vb)
    # print("句子相似度为：")
    sim = (sum(va * vb) / math.sqrt(sum(va * va) + sum(vb * vb)))
    # print(sim)
    return sim

def ci(c):
    model_1 = word2vec.Word2Vec.load("standard.model")
    y2 = model_1.most_similar(c, topn=10)  # 10个最相关的
    print("和",c,"最相关的词有：\n")
    for item in y2:
        print(item[0], item[1])

def xiangsi(quest):
    quest = jieba.cut(quest)
    for i in quest:
        try:
            ci(i)
        except Exception as e:
            pass

def read_from_stand():
    ret = 0
    rep = ''
    open = codecs.open('question_standard.csv', 'r', encoding='utf_8_sig')
    csv_file = csv.reader(open)
    quest = input('您的问题？')

    quest = ' '.join(jieba.cut(quest))
    for i in csv_file:
        quest_ = ' '.join(jieba.cut(i[0]))
        sim = bidui(quest, quest_)
        if sim > ret and sim > 0.15:
            ret = sim
            rep = i
            print("目前最佳匹配是：", rep[0], "匹配度是：", ret)
            print(rep[1])


def test_answer(request):
    ret = 0
    rep = ''
    quest = request.POST['question']
    quest = ' '.join(jieba.cut(quest))
    qas = QuestionAnswer.objects.all()
    print(quest)
    cache = []
    sim_keys = []
    for qa in qas:
        quest_ = ' '.join(jieba.cut(qa.question))
        sim = bidui(quest, quest_)
        # print(cache)
        if len(cache) < 5:
            cache.append({'sim': sim, 'obj': qa})
            print("目前入队是：", qa.question, "匹配度是：", sim)
        elif len(cache) == 5:
            cache = sorted(cache, key=lambda s: s['sim'])
            if sim > cache[0]['sim']:
                tmp = cache[0]['sim']
                cache.pop(0)
                cache.append({'sim': sim, 'obj': qa})
                print(sim, "替换", tmp)
    cache = sorted(cache, key=lambda s: s['sim'], reverse=True)
    l = []
    for c in cache:
        tmp = {}
        tmp['sim'] = c['sim']
        tmp['question'] = c['obj'].question
        tmp['answer'] = c['obj'].answer
        l.append(tmp)
    cache = {'cache': l}
    return HttpResponse(json.dumps(cache), content_type='application/json')



def for_app(request):
    return render(request, 'question-client/forapp.html')
