import pickle
import argparse
import logging
import json
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS
import difflib

try:
    from flask_restplus import Namespace, Resource, Api
except:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Namespace, Api, Resource

from flask_restplus import reqparse
from numpy.linalg import norm
from sklearn.neighbors import NearestNeighbors
from os import listdir
from os.path import isfile, join
from collections import defaultdict

app = Flask(__name__)
CORS(app)
api = Api(app=app)
ns_conf = api.namespace('knowledgegraph', description='methods')

parser = argparse.ArgumentParser(description='Argument Parser')
parser.add_argument('--data', type=str, default="../../data", help='Data path')
parser.add_argument('--rec_data', type=str, default="../../rec_data", help='Rec Data path')
args = parser.parse_args()

id_parser = reqparse.RequestParser()
id_parser.add_argument('id', type=str, help='doc id')

rec_parser = reqparse.RequestParser()
rec_parser.add_argument('target_query', help='query word')
rec_parser.add_argument('model_query', help='query rec model: air or hpe')


def rec_loader(modelname, taskname):
    train_dict = defaultdict(list)
    filename = 'adkg.'+str(modelname)+'.rep.'+str(taskname)+'.rec'
    with open(join( args.rec_data, filename), 'r') as f:
        for line in f:
            line = line.split("\t")
            train_dict[str(line[0])] = line[1:]
    return train_dict

def pkl_loader():
    train_dict = {}
    id_to_idx = {}
    onlyfiles = [f for f in listdir(args.data) if isfile(join(args.data, f))]
    for _, filename in enumerate(onlyfiles):
        with open(join( args.data, filename), 'rb') as f:
            train_dict = pickle.load(f)
    for idx, i in enumerate(train_dict['PubmedArticleSet']['PubmedArticle']):
        id_num = i['MedlineCitation']['PMID']['#text']
        id_to_idx[str(id_num)] = idx
    return train_dict['PubmedArticleSet']['PubmedArticle'], id_to_idx

@ns_conf.route('/details')
class id(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()

        try:
            idx = int(id_to_idx[args['id']])

            '''Abstract'''
            abs_text = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            if isinstance(abs_text, list):
                abs_text_str = ""
                for subtext in abs_text:
                    subtext = subtext["#text"]
                    subtext += " "
                    abs_text_str += subtext
            else:
                abs_text_str = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            
            if not isinstance(abs_text_str, str):
                abs_text_str = abs_text_str["#text"]

            '''Title'''
            title_text_prefix = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']
            if isinstance(title_text_prefix, str):
                title_text = title_text_prefix
            else:
                try:
                    title_text = title_text_prefix['#text'][:-1] + title_text_prefix['i']
                except:
                    title_text = title_text_prefix['#text']

            '''Author'''
            author_dict = train_dict[idx]['MedlineCitation']['Article']['AuthorList']['Author']

            '''Keyword'''
            keyword_list = []

            if "KeywordList" in train_dict[idx]['MedlineCitation'].keys():
                for keyword_dict in train_dict[idx]['MedlineCitation']["KeywordList"]["Keyword"]:
                    keyword_list.append(keyword_dict["#text"])
            if len(keyword_list) == 0:
                keyword_list.append("No keywords")

            '''NIH URL'''
            infolist = train_dict[idx]['PubmedData']['ArticleIdList']['ArticleId']
            key_buf = [x["@IdType"] for x in infolist]
            nih_url = ""

            doi = ""
            if "doi" in key_buf:
                idx = key_buf.index("doi")
                doi = infolist[idx]["#text"]

            pubmed = ""
            if "pubmed" in key_buf:
                idx = key_buf.index("pubmed")
                pubmed = infolist[idx]["#text"]
                nih_url = "https://pubmed.ncbi.nlm.nih.gov/" + pubmed

            '''Download URL'''
            download_url = ""
            pmc_id = ""
            if "pmc" in key_buf:
                idx = key_buf.index("pmc")
                pmc_id = infolist[idx]["#text"]
                download_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/" + pmc_id + "/?report=reader"

            return jsonify({
                    'given': args['id'],
                    'title': title_text,
                    'abstract': abs_text_str,
                    'author_list': author_dict,
                    'pmid': pubmed,
                    'pmcid': pmc_id,
                    'doi': doi,
                    'keyword': keyword_list,
                    'download_url': download_url,
                    'nih_url': nih_url,
                })
        except:
            return 'ID Not Found'

@ns_conf.route('/w2p')
class w2p(Resource):
    @ns_conf.doc(parser=rec_parser)
    def get(self):
        args = rec_parser.parse_args()
        key_word_org = args['target_query']
        model_word = args['model_query']
        doc_dict, id_to_idx = pkl_loader()
        train_dict = rec_loader(model_word, "iu")
        train_dict_key = list(train_dict.keys())

        if key_word_org in train_dict_key:
            key_word = key_word_org
        else:
            near_key_word = difflib.get_close_matches(key_word_org, train_dict_key)
            try:
                key_word = near_key_word[0]
            except:
                key_word = 'Alzheimer’s'
                near_key_word = difflib.get_close_matches(key_word, train_dict_key)
                key_word = near_key_word[0]
        str_rec_list = [str(x).rstrip() for x in train_dict[key_word]]

        str_title_rec_list = []
        str_url_rec_list = []
        for pid in train_dict[key_word]:
            pid = str(pid).rstrip()
            idx = int(id_to_idx[pid])

            # Paper URL
            infolist = doc_dict[idx]['PubmedData']['ArticleIdList']['ArticleId']
            key_buf = [x["@IdType"] for x in infolist]
            nih_url = ""
            if "pubmed" in key_buf:
                key_idx = key_buf.index("pubmed")
                pubmed = infolist[key_idx]["#text"]
                nih_url = "https://pubmed.ncbi.nlm.nih.gov/" + pubmed

            # Paper Title
            title_text_prefix = doc_dict[idx]['MedlineCitation']['Article']['ArticleTitle']
            if isinstance(title_text_prefix, str):
                title_text = title_text_prefix
            else:
                try:
                    title_text = title_text_prefix['#text'][:-1] + title_text_prefix['i']
                except:
                    title_text = title_text_prefix['#text']

            str_title_rec_list.append(title_text)
            str_url_rec_list.append(nih_url)


        return jsonify({
                'given_word': key_word_org,
                'given_model': model_word,
                'rec_id_result': str_rec_list[:6],
                'rec_title_result': str_title_rec_list[:6],
                'rec_url_result': str_url_rec_list[:6]
            })


@ns_conf.route('/w2w')
class w2w(Resource):
    @ns_conf.doc(parser=rec_parser)
    def get(self):
        args = rec_parser.parse_args()
        key_word_org = args['target_query']
        model_word = args['model_query']
        train_dict = rec_loader(model_word, "ii")
        train_dict_key = train_dict.keys()

        if key_word_org in train_dict_key:
            key_word = key_word_org
        else:
            near_key_word = difflib.get_close_matches(key_word_org, train_dict_key)
            try:
                key_word = near_key_word[0]
            except:
                key_word = 'Alzheimer’s'
                near_key_word = difflib.get_close_matches(key_word, train_dict_key)
                key_word = near_key_word[0]

        str_rec_list = [str(x).lower().rstrip().replace("-", " ") for x in train_dict[key_word] if not x.isnumeric()]


        return jsonify({
                'given_word': key_word_org,
                'given_model': model_word,
                'rec_result': str_rec_list[:20]
            })


@ns_conf.route('/id2abs')
class id2abs(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()

        try:
            idx = int(id_to_idx[args['id']])
            abs_text = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            if isinstance(abs_text, list):
                abs_text_str = ""
                for subtext in abs_text:
                    subtext = subtext["#text"]
                    subtext += " "
                    abs_text_str += subtext
            else:
                abs_text_str = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            title_text = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']

            return jsonify({
                'given': args['id'],
                'title': title_text,
                'abstract': abs_text_str
            })
        except:
            return 'ID Not Found'

@ns_conf.route('/id2author')
class id2author(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()
        try:
            idx = int(id_to_idx[args['id']])
            author_dict = train_dict[idx]['MedlineCitation']['Article']['AuthorList']['Author']
            title_text = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']
            return jsonify({
                'given': args['id'],
                'title': title_text,
                'auther_list': author_dict
            })
        except:
            return 'ID Not Found'


@ns_conf.route('/id2keyword')
class id2keyword(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()

        try: # 30569483 # not all of the article has a keyword list

            idx = int(id_to_idx[args['id']])

            abs_text = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            if isinstance(abs_text, list):
                abs_text_str = ""
                for subtext in abs_text:
                    subtext = subtext["#text"]
                    subtext += " "
                    abs_text_str += subtext
            else:
                abs_text_str = train_dict[idx]['MedlineCitation']['Article']['Abstract']['AbstractText']
            title_text = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']

            keyword_list = []

            if "KeywordList" in train_dict[idx]['MedlineCitation'].keys():
                for keyword_dict in train_dict[idx]['MedlineCitation']["KeywordList"]["Keyword"]:
                    keyword_list.append(keyword_dict["#text"])

            return jsonify({
                'given': args['id'],
                'title': title_text,
                'abstract': abs_text_str,
                'keyword': keyword_list,
            })
        except:
            return 'ID Not Found'


@ns_conf.route('/id2downloadurl')
class id2downloadurl(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()

        try: # 31825506 # not all of the article has a url

            idx = int(id_to_idx[args['id']])
            title_text = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']

            infolist = train_dict[idx]['PubmedData']['ArticleIdList']['ArticleId']
            key_buf = [x["@IdType"] for x in infolist]
            url = None

            if "pii" in key_buf:
                idx = key_buf.index("pii")
                pii_id = infolist[idx]["#text"]
                url = "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/" + pii_id

            return jsonify({
                'given': args['id'],
                'title': title_text,
                'download_url': url
            })
        except:
            return 'ID Not Found'


@ns_conf.route('/id2nihurl')
class id2nihurl(Resource):
    @ns_conf.doc(parser=id_parser)
    def get(self):
        train_dict, id_to_idx = pkl_loader()
        args = id_parser.parse_args()

        try: # 31825506 # not all of the article has a url

            idx = int(id_to_idx[args['id']])
            title_text = train_dict[idx]['MedlineCitation']['Article']['ArticleTitle']

            infolist = train_dict[idx]['PubmedData']['ArticleIdList']['ArticleId']
            key_buf = [x["@IdType"] for x in infolist]
            url = None

            if "pmc" in key_buf:
                idx = key_buf.index("pmc")
                pmc_id = infolist[idx]["#text"]
                url = "https://www.ncbi.nlm.nih.gov/pmc/articles/" + pmc_id + "/?report=reader"

            return jsonify({
                'given': args['id'],
                'title': title_text,
                'NIH_url': url
            })
        except:
            return 'ID Not Found'

def dict_all(data):
    if isinstance(data, dict):
        for k, v in data.items():
            print(k, end=" -> ")
            dict_all(v)


    elif isinstance(data, (list, tuple, set)):
        for v in data:
            dict_all(v)
    else:
        if data is not None and "suzuki_2019_oi_190654.pdf" in data:  # "2757375" in data:
            print(data)
            print("")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5566)
