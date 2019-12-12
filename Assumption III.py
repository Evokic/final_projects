"""
Data Source:
- https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/
- https://www.census.gov/data/tables/time-series/demo/educational-attainment/cps-historical-time-series.html

"""
import pandas as pd
import numpy as np
from scipy import stats
from operator import itemgetter
import matplotlib.pyplot as plt

# reading files
unemployment = pd.read_csv('data/Unemployment.csv')
edu_att = pd.read_csv('data/EducationAttainment.csv', na_values='X')

# Data Preparation and Preprocessing
unemployment = unemployment.dropna(how='all')
loc_info = unemployment.iloc[:, 0:3].reset_index()
un_num = unemployment.loc[:, unemployment.columns.str.contains('Unemployed')].reset_index()
un_rate = unemployment.loc[:, unemployment.columns.str.contains('Unemployment')].reset_index()
un_num = pd.merge(loc_info, un_num, on='index', how='left').drop(['index'], axis=1)
un_rate = pd.merge(loc_info, un_rate, on='index', how='left').drop(['index'], axis=1)
un_rate_state = un_rate.groupby('State').mean().reset_index().drop(['FIPS'], axis=1)
edu_info = edu_att.iloc[:, 0].reset_index()
edu_att_num = edu_att.loc[:, edu_att.columns.str.contains('Num')].reset_index()
edu_att_rate = edu_att.loc[:, edu_att.columns.str.contains('Percent')].reset_index()
edu_att_num = pd.merge(edu_info, edu_att_num, on='index', how='left').drop(['index'], axis=1)
edu_att_rate = pd.merge(edu_info, edu_att_rate, on='index', how='left').drop(['index'], axis=1)
edu_att_num = edu_att_num.drop(index=edu_att_num.loc[(edu_att_num['Detailed years of school'] == 'Total')].index) \
    .reset_index().drop(['index'], axis=1)
un_num_state = un_num.drop(['FIPS', 'Area_name'], axis=1)
un_num_state = un_num_state.drop(index=un_num_state.loc[(un_num_state['State'] == 'US')].index)
un_num_state = un_num_state.groupby('State').sum().reset_index()


def NormalTest_Result(data):
    """Given certain data of a variable, return whether it comes from a normal distribution.
       All Nan values are ignored.
       Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.normaltest.html

    :param data: certain amount of data of a variable, should be array-like
    :return: the result whether the data is following a normal distribution.

    >>> np.random.seed(123)
    >>> k1 = np.random.normal(5, 10, size=500)
    >>> NormalTest_Result(k1)
    'True. The data is normally distributed.'
    >>> k2 = [1, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1]
    >>> NormalTest_Result(k2)
    'False. The data is not normally distributed.'
    """
    k2, p = stats.normaltest(data, nan_policy='omit')
    if p > 0.05:
        r = 'True. The data is normally distributed.'
    else:
        r = 'False. The data is not normally distributed.'
    return r


def Pearson_co(var1, var2):
    """ Given two variables with the same length of recorded data each stored in a list,
    calculate Pearson correlation coefficient between them.
    Reference:https://en.wikipedia.org/wiki/Pearson_correlation_coefficient

    :param var1: a variable with recorded data stored in a list
    :param var2: a variable with recorded data stored in a list (same length as var1)
    :return: Pearson correlation coefficient between two given variables.

    >>> var1=[10, 20, 30, 50, 80]
    >>> var2=[0.11, 0.12, 0.13, 0.15, 0.18]
    >>> round(Pearson_co(var1, var2), 1)
    1.0
    """
    s1 = 0
    if len(var1) == len(var2):
        for i in range(len(var1)):
            s1 += var1[i] * var2[i]
        E_v1v2 = s1 / len(var1)
        E_v1 = sum(var1) / len(var1)
        E_v2 = sum(var2) / len(var2)
        std_v1 = np.std(var1)
        std_v2 = np.std(var2)
        P = (E_v1v2 - E_v1 * E_v2) / (std_v1 * std_v2)
    else:
        print('The length of the two variables must be the same.')
    return P


def output(sorted_list):
    """Given a sorted list with Pearson correlation coefficient between two variables and their related index for state
    and educational info, then refer to the dataframes and return the output in a certain form.

    :param sorted_list: a sorted list with Pearson correlation coefficient between two variables
    :return: a table-like output of the sorted list
    """
    print('{0:^10}{1:^60}{2:^31}'.format('State', 'Detailed years of school', 'Pearson correlation coefficient'))
    for m in sorted_list:
        print('{0:^10}{1:^60}{2:^33.3f}'.format(un_num_state['State'][m[2]],
                                                edu_att_num['Detailed years of school'][m[4]], m[0]))


def Normalize(data_list):
    """Given a list containing certain amount of data,
    normalize the data in the list and return a list containing all the normalized data.

    :param data_list: a list containing certain amount of data
    :return: a list containing all the normalized data.

    >>> a=[1, 2, 3]
    >>> Normalize(a)
    [0.0, 0.5, 1.0]
    >>> b=[0, 1, 3, 10, 3]
    >>> Normalize(b)
    [0.0, 0.1, 0.3, 1.0, 0.3]
    """
    norm_list = []
    for n in data_list:
        n_norm = (n - min(data_list)) / (max(data_list) - min(data_list))
        norm_list.append(n_norm)
    return norm_list


def line_plot(sorted_list):
    """Give a sorted list containing two variables' related index for state and educational info from 2007-2019,
     the unemployment number and number of different educational attainment. Return the line plot using
     the normalized variables.

    :param sorted_list: a sorted list containing two variables' related index for state and educational info
    :return: a line plot using the normalized variables.
    """
    years = range(2007, 2019)
    for i in sorted_list:
        un = pd.Series(
            Normalize(list(un_num_state[un_num_state['State'] == un_num_state['State'][i[2]]].values[0][1:])),
            index=years)
        edu_att = pd.Series(Normalize(list(edu_att_num.iloc[sorted_list[2][4], 1:13].sort_index())), index=years)
        plt.rcParams["figure.dpi"] = 100
        with plt.style.context('seaborn'):
            plt.figure()
            plt.plot(un, linewidth=3, label=un_num_state['State'][i[2]] + '_Unemployment')
            plt.plot(edu_att, linewidth=3, label=edu_att_num['Detailed years of school'][i[4]])
            plt.xlabel("Year")
            plt.ylabel("The normalized value")
            plt.yscale("linear")
            plt.legend()
            plt.show()


def check_distribution(normaltest_result):
    """Give a list containing the results of normal distribution test,
    return 1 if the result if 'True. ...comes from a normal distribution' or 0 if 'False, ... does not not come from
    a normal distribution.'

    :param normaltest_result: a list containing the results of normal distribution test
    :return: 1 if the result if 'True. ...comes from a normal distribution' or 0 if 'False....'

    >>> result1='False'
    >>> check_distribution(result1)
    0
    >>> result2='True. It is following a normal distribution'
    >>> check_distribution(result2)
    1
    """
    if 'False' in normaltest_result:
        check = 0
    else:
        check = 1
    return check


if __name__ == '__main__':
    P_list = []
    for k in range(un_num_state.shape[0]):
        un_list = list(un_num_state.iloc[k, 1:])    # get unemployment number
        if check_distribution(NormalTest_Result(un_list)) == 1:
            pass
        else:
            print('The data from State: ', un_num_state.iloc[k, 0], " does not follow a normal distribution.")
        # If certain state's data is not normally distributed, the result of this state will be ignored.
        # For the n>=20 sample number warning, since the data in this project is only from 2007-2018,
        # this warning may occur.
        for i in range(edu_att_num.shape[0]):
            edu_list = list(edu_att_num.iloc[i, 1:13].sort_index())    # get educational level for different years
            P_co = Pearson_co(un_list, edu_list)
            if not np.isnan(P_co):
                P_list.append([P_co, 'un_num_state:', k, 'edu_att_num:', i])
    P_sorted = sorted(P_list, key=itemgetter(0))
    Neg_5 = P_sorted[0:5]   # Top five negative Pearson correlation coefficient
    Pos_5 = P_sorted[-1:-6:-1]  # Top five positive Pearson correlation coefficient
    output(Neg_5)
    output(Pos_5)
    line_plot(Neg_5)
    line_plot(Pos_5)

