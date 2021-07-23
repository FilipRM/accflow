import pandas as pd
import math


def zero_check_ib(data):
    x = data.where(data.PeriodNr == 0).Value.sum()
    return x


def zero_check_year(data):
    y = data.groupby(["Year"])["Value"].sum()
    return y


def extract_firsts(data):
    temp_data = data.copy()
    temp_data.Value = temp_data.Value.astype(str).str.replace("-", "")
    firsts = list(temp_data.Value.str[0])
    return firsts


def act_dist(data):
    numbers = act_obs(data)
    percentages = []

    for i in range(0, 9):
        percentages.append(numbers[i] / sum(numbers))
    return percentages


def act_obs(data):
    numbers = []
    for i in range(1, 10):
        numbers.append(extract_firsts(data).count(str(i)))
    return numbers


def graph_plot(data):
    percentages = act_dist(data)
    expected = exp_dis()

    data_comparison = pd.DataFrame({"Expected": expected, "Actual": percentages}, index=range(1, 10))

    data_comparison.plot.bar()

    return data_comparison


def exp_dis():
    expected = [math.log10(1 + 1 / d) for d in range(1, 10)]
    return expected


def benford_test(data):
    observed = act_obs(data)
    expected = []

    for i in range(len(observed)):
        expected.append(exp_dis()[i] * sum(observed))

    chi_square_stat = 0;  # chi-square test statistic
    for data, expected in zip(observed, expected):
        chi_square = math.pow(data - expected, 2)
        chi_square_stat += chi_square / expected

    return chi_square_stat < 15.51  # 5% p-value confidence statistic

