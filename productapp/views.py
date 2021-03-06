import pandas as pd
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from gensim.models import Doc2Vec

from productapp.forms import ProductCreationForm
from productapp.models import Product, Category
from reviewapp.forms import ReviewCreationForm



class ProductList(ListView):
    model = Product
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    form_class = ReviewCreationForm
    context_object_name = 'target_product'
    template_name = 'productapp/product_detail.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreationForm
    template_name = 'productapp/create.html'
    # models.category_id = 2
    # def form_valid(self, form):
    #     form.instance.writer = self.request.user
    #     return super().form_valid(form)

    def form_valid(self, form):
        # form.instance.product_id = self.request.POST.get('product_pk')
        # form.instance.writer = self.request.user
        self.object = form.save(commit=False)
        output = category_result(self.object.name)
        self.object.category_id = output
        self.object.save()
        return super().form_valid(form)


    def get_success_url(self):
        # writer = self.request.user
        # writer.profile.mileage += 10
        # writer.profile.save()
        return reverse('productapp:list')
# def index(request):
#     # 가장 최근에 등록된 상품부터 나열
#     products = Product.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'productapp/product_list.html',
#         {
#             'products': products,
#         }
#     )

# def single_product_page(request, pk):
#     product = Product.objects.get(pk=pk)
#
#     return render(
#         request,
#         'productapp/product_detail.html',
#         {
#             'product': product,
#         }
#     )

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    product_list = Product.objects.filter(category=category)

    return render(
        request,
        'productapp/product_list.html',
        {
            'product_list':product_list,
            'categories':Category.objects.all(),
            'category':category,
        }
    )


import csv

import numpy as np
from django.shortcuts import render
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from konlpy.tag import Okt

okt = Okt()
model = load_model('models/category_best_model.h5')

vocab_size = 5748
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게', '인기', '짱', '강력', '추천', '선물', '특가', '할인', '세일', '생일', '기념일']
category_dict = {0: '먹거리', 1: '패션', 2: '잡화', 3: '쥬얼리', 4: '인테리어 소품', 5: '생활', 6: '기타'}

product_data = []
path = 'data/category_train.csv'

with open(path, 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    for idx, list in enumerate(reader):
        product_data.append(list)

max_len = 15
tokenizer = Tokenizer(vocab_size)
tokenizer.fit_on_texts(product_data)

def category_result(full):
    full = full
    full = okt.morphs(full)
    full = [word for word in full if not word in stopwords]
    encoded = tokenizer.texts_to_sequences([full])
    # error !!!!
    pad_new = pad_sequences(encoded, maxlen=15)
    score = (model.predict(pad_new))
    output = score.argmax() if score.max() > 0.22 else 6
    output += 1
    return output

def similar(request, id):
    df = pd.read_pickle('data/original_data.pkl')
    model = Doc2Vec.load('models/similar_model')
    id = id
    name = ''.join(df[df['id'] == id]['name'])
    label = int(df[df['id'] == id]['label'])

    # name = name
    # id = int(df[df['name'] == name]['id'])
    # label = int(df[df['name'] == name]['label'])

    similar = model.docvecs.most_similar(str(id), topn=15)

    sim_ids= []
    sim_names = []
    for sim in similar:
        sim_id = int(sim[0])
        sim_name = ''.join(df[df['id'] == sim_id]['name'])
        sim_label = int(df[df['id'] == sim_id]['label'])
        if label == sim_label:
            sim_ids.append(sim_id)
            sim_names.append(sim_name)
    return render(request, 'productapp/result.html', {'search_sent': name, 'name': sim_names})