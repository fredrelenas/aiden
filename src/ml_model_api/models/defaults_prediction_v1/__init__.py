from sklearn.base import BaseEstimator, TransformerMixin


class DefaultsModelPreProcessing(BaseEstimator, TransformerMixin):
    """
    Custom preprocessor to encode categorical features
    """

    def __init__(self):
        self.continuous_vars = selected_continuous_vars
        self.multi_cat_vars = selected_multi_cat_vars
        self.bi_cat_vars = selected_bi_cat_vars
        self.embed_dict = embed_dict_prod
        self.dict_encrypt = dict_encrypt
        self.x_train_columns = X_train.columns

        self.feature_list = self.continuous_vars + self.multi_cat_vars + self.bi_cat_vars

    def transform(self, df_in, y=0):
        df = df_in[self.feature_list]
        df['Requested Duration'] = df['Requested Duration'].apply(lambda x: int(x.strip('months')))
        df['adverse-on-file'] = df['adverse-on-file'].apply(
            lambda x: 'Y' if str(x) == 'Yes' else ('N' if str(x) == 'No' else x))
        df[self.bi_cat_vars] = df[self.bi_cat_vars].apply(lambda x: self.dict_encrypt[x.name].transform(x))
        for feat in self.multi_cat_vars:
            df[feat] = df[feat].apply(lambda x: self.embed_dict[feat][str(x)])

        # Below line ensures that the column order in the df is the same as in the X_train.
        # This avoids "feature_names mismatch when using xgboost + sklearn" error
        df = df[self.x_train_columns]
        return df

    def fit(self, df, y=0):
        # df[self.encode_list].astype(str).apply(lambda x: self.dict_encrypt[x.name].fit(x))
        return self