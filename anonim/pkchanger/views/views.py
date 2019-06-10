
import pandas as pd
from django.shortcuts import render
import os
from ..forms import UploadFileForm
from django.views.generic import View
from django.contrib import messages
from . import generalize, csv


# TODO:configどうするか
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../media/'
FILENAME = 'data.csv'
CARDINALITY = 0.98
AGE_STRING = ['age', 'nen', 'yearsOld']
LOCATION_STRING = ['location', 'address']


class IndexView(View):
    form_class = UploadFileForm
    template_name = 'pkchanger/index.html'
    df = pd.DataFrame()
    bl_uploaded = False

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form_class()
        context['uploaded'] = IndexView.bl_uploaded = False
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form_class(request.POST, request.FILES)

        # downloadする
        if 'export_csv' in request.POST:
            if (IndexView.df.empty):
                messages.error(self.request, 'Not Found')
                return render(request, self.template_name, context)
            return csv.export_csv(IndexView.df)
        elif 'generalize' in request.POST:
            self.generalize(request)
        elif 'k-anonim' in request.POST:
            self.k_anonim(request)
        elif 'show_identifier' in request.POST:
            self.show_identifier(request)
        elif 'hiding' in request.POST:
            self.hiding(request)
        elif 'readFile' in request.POST:
            path = os.path.join(UPLOADE_DIR, FILENAME)
            if context['form'].is_valid():
                # 書き込み
                csv.import_csv(request, path)
                # 読み出し
                IndexView.df = pd.read_csv(path, sep=',', header=0)

        IndexView.bl_uploaded = True
        context['df'] = IndexView.df
        context['uploaded'] = IndexView.bl_uploaded
        return render(request, self.template_name, context)

    def hiding(self, request):
        """masking selected item

        Arguments:
            request {[type]} -- [description]
        """
        self.make_hiding_of_selected_data(
            request.POST.getlist('checkedCol'), IndexView.df)
        messages.success(self.request, "要素を*に変更し、匿名化しました")

    def show_identifier(self, request):
        """Display the item of the identifier

        Arguments:
            request {[type]} -- [description]
        """
        identifiers = self.list_of_identifier_columns(IndexView.df)
        if identifiers is None:
            return
        id_msg = ""
        for i in range(len(identifiers)):
            if i != 0:
                id_msg += ", "
            id_msg += identifiers[i]
        msg = "識別子候補は次の通りです(" + str(CARDINALITY) + \
            "以上の固有性)：" + id_msg
        messages.success(self.request, msg)

    def k_anonim(self, request):
        """show k-anonymity

        Arguments:
            request {[type]} -- [description]
        """
        if (IndexView.df.empty):
            messages.error(self.request, 'Not Found')
            return
        # チェックされているかチェック
        checkedCol = request.POST.getlist('checkedCol')
        if not checkedCol:
            messages.error(self.request, 'Not Checked')
            return

        # anonimizeカウント
        k_anonimize_count = self.k_anonimize_count(
            checkedCol, IndexView.df)
        msg = "選択項目のk-匿名化は以下の通りになります\n" + str(k_anonimize_count) + \
            "分の1以上の固有性)："
        messages.info(self.request, msg)

    def generalize(self, request):
        """Generalize selected items using generalization techniques

        Arguments:
            request {[type]} -- [description]
        """
        checkedCol = request.POST.getlist('checkedCol')
        for col in checkedCol:
            if col in AGE_STRING:
                for i in range(len(IndexView.df[col])):
                    IndexView.df.loc[i, col] = generalize.age_range(
                        IndexView.df[col][i])
            if col in LOCATION_STRING:
                for i in range(len(IndexView.df[col])):
                    IndexView.df.loc[i, col] = generalize.locale(
                        IndexView.df[col][i])
                print("位置情報の一般化")

    # 関数とかどこに書くのがいいのかあとで調べる
    def k_anonimize_count(self, selected_columns, dataframe):
        lists = []
        for i in range(len(dataframe)):
            val = ''
            for column in selected_columns:
                val += str(dataframe[column][i])
            lists.append(val)
        return len(list(set(lists)))

    def list_of_identifier_columns(self, dataframe):
        lists = []
        for c in dataframe.columns:
            org_list = dataframe[c].tolist()
            unique_list = list(set(org_list))
            if len(unique_list) / len(org_list) > CARDINALITY:
                lists.append(c)
        if len(lists) == 0:
            return None
        return lists

    def make_hiding_of_selected_data(self, columns, dataframe):  # 命名規則調べる
        for column in columns:
            for i in range(len(dataframe[column])):
                dataframe[column][i] = "*"
