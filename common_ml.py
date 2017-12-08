import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def order_features_by_gains1(model, importance_type='weight'):
    if str(type(model)) != "<class 'xgboost.core.Booster'>":
        sorted_feats = sorted(model._Booster.get_score(importance_type=importance_type).items(), key=lambda k: -k[1])
    else:
        sorted_feats = sorted(model.get_score(importance_type=importance_type).items(), key=lambda k: -k[1])
    return sorted_feats


def getFeaturesImportance1(fnames, model, importance_type='weight'):
    # Feature importance values
    model_fi = pd.DataFrame(fnames)
    model_fi.columns = ['feature']
    ff_gain = order_features_by_gains1(model, importance_type=importance_type)
    ff = np.zeros(len(fnames))
    for k, v in ff_gain:
        ff[fnames.index(k)] = v
    model_fi['importance'] = 100.0 * (ff / ff.max())
    return model_fi.sort_values('importance', ascending=0)


def drawFeaturesImportancePlot(model_fi, topN):
    pos = np.arange(topN)[::-1] + 1
    topn_features = list(model_fi.sort_values('importance', ascending=0)['feature'].head(topN))

    plt.figure(figsize=(6, 6))
    plt.axis([0, 100, 0, topN + 1])
    plt.barh(pos, model_fi.sort_values('importance', ascending=0)['importance'].head(topN), align='center')
    plt.yticks(pos, topn_features)

    axes = plt.gca()
    colors = ['red'] * 10 + ['blue'] * 10
    for color, tick in zip(colors, axes.yaxis.get_major_ticks()):
        tick.label1.set_color(color)  # set the color property

    plt.xlabel('Relative Importance')
    plt.grid()
    plt.title('Model Feature Importance Plot', fontsize=20)
    plt.show()

def drawFeaturesImportancePlot2(model_fi_1, model_fi_2, topN, names=None):
    plt.figure(figsize=(15, 6))

    pos = np.arange(topN)[::-1] + 1
    topn_features = list(model_fi_1.sort_values('importance', ascending=0)['feature'].head(topN))

    plt.subplot(1, 2, 1)
    plt.axis([0, 100, 0, topN + 1])
    plt.barh(pos, model_fi_1.sort_values('importance', ascending=0)['importance'].head(topN), align='center')
    plt.yticks(pos, topn_features)

    axes = plt.gca()
    colors = ['red'] * 10 + ['blue'] * 10
    for color, tick in zip(colors, axes.yaxis.get_major_ticks()):
        tick.label1.set_color(color)  # set the color property

    plt.xlabel('Relative Importance')
#    plt.grid()
    plt.title('' if names is None else names[0], fontsize=15)

    topn_features = list(model_fi_2.sort_values('importance', ascending=0)['feature'].head(topN))

    plt.subplot(1, 2, 2)
    plt.axis([0, 100, 0, topN + 1])
    plt.barh(pos, model_fi_2.sort_values('importance', ascending=0)['importance'].head(topN), align='center')
    plt.yticks(pos, topn_features)

    axes = plt.gca()
    colors = ['red'] * 10 + ['blue'] * 10
    for color, tick in zip(colors, axes.yaxis.get_major_ticks()):
        tick.label1.set_color(color)  # set the color property

    plt.xlabel('Relative Importance')
#    plt.grid()
    plt.title('' if names is None else names[1], fontsize=15)
    plt.suptitle('Model Feature Importance Plot', fontsize=20)
    #plt.subplots_adjust(top=0.85)
    plt.tight_layout(rect=[0, 0.02, 1, 0.98])
    plt.show()