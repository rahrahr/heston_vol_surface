import unittest
import heston
import utils
import QuantLib as ql
import pandas as pd
import numpy as np
from termcolor import colored

# some test data.
day_count = heston.get_day_count()
calendar = heston.get_calendar()

calculation_date = ql.Date(6, 11, 2015)

spot = 659.37
ql.Settings.instance().evaluationDate = calculation_date

dividend_yield = ql.QuoteHandle(ql.SimpleQuote(0.0))
risk_free_rate = 0.01
dividend_rate = 0.0
flat_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, risk_free_rate, day_count))
dividend_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, dividend_rate, day_count))

expiration_dates = [ql.Date(6, 12, 2015), ql.Date(6, 1, 2016), ql.Date(6, 2, 2016),
                    ql.Date(6, 3, 2016), ql.Date(
    6, 4, 2016), ql.Date(6, 5, 2016),
    ql.Date(6, 6, 2016), ql.Date(
    6, 7, 2016), ql.Date(6, 8, 2016),
    ql.Date(6, 9, 2016), ql.Date(
    6, 10, 2016), ql.Date(6, 11, 2016),
    ql.Date(6, 12, 2016), ql.Date(
    6, 1, 2017), ql.Date(6, 2, 2017),
    ql.Date(6, 3, 2017), ql.Date(
    6, 4, 2017), ql.Date(6, 5, 2017),
    ql.Date(6, 6, 2017), ql.Date(
    6, 7, 2017), ql.Date(6, 8, 2017),
    ql.Date(6, 9, 2017), ql.Date(6, 10, 2017), ql.Date(6, 11, 2017)]

strikes = [527.50, 560.46, 593.43, 626.40,
           659.37, 692.34, 725.31, 758.28]
iv = [
    [0.37819, 0.34177, 0.30394, 0.27832, 0.26453, 0.25916, 0.25941, 0.26127],
    [0.3445, 0.31769, 0.2933, 0.27614, 0.26575, 0.25729, 0.25228, 0.25202],
    [0.37419, 0.35372, 0.33729, 0.32492, 0.31601, 0.30883, 0.30036, 0.29568],
    [0.37498, 0.35847, 0.34475, 0.33399, 0.32715, 0.31943, 0.31098, 0.30506],
    [0.35941, 0.34516, 0.33296, 0.32275, 0.31867, 0.30969, 0.30239, 0.29631],
    [0.35521, 0.34242, 0.33154, 0.3219, 0.31948, 0.31096, 0.30424, 0.2984],
    [0.35442, 0.34267, 0.33288, 0.32374, 0.32245, 0.31474, 0.30838, 0.30283],
    [0.35384, 0.34286, 0.33386, 0.32507, 0.3246, 0.31745, 0.31135, 0.306],
    [0.35338, 0.343, 0.33464, 0.32614, 0.3263, 0.31961, 0.31371, 0.30852],
    [0.35301, 0.34312, 0.33526, 0.32698, 0.32766, 0.32132, 0.31558, 0.31052],
    [0.35272, 0.34322, 0.33574, 0.32765, 0.32873, 0.32267, 0.31705, 0.31209],
    [0.35246, 0.3433, 0.33617, 0.32822, 0.32965, 0.32383, 0.31831, 0.31344],
    [0.35226, 0.34336, 0.33651, 0.32869, 0.3304, 0.32477, 0.31934, 0.31453],
    [0.35207, 0.34342, 0.33681, 0.32911, 0.33106, 0.32561, 0.32025, 0.3155],
    [0.35171, 0.34327, 0.33679, 0.32931, 0.3319, 0.32665, 0.32139, 0.31675],
    [0.35128, 0.343, 0.33658, 0.32937, 0.33276, 0.32769, 0.32255, 0.31802],
    [0.35086, 0.34274, 0.33637, 0.32943, 0.3336, 0.32872, 0.32368, 0.31927],
    [0.35049, 0.34252, 0.33618, 0.32948, 0.33432, 0.32959, 0.32465, 0.32034],
    [0.35016, 0.34231, 0.33602, 0.32953, 0.33498, 0.3304, 0.32554, 0.32132],
    [0.34986, 0.34213, 0.33587, 0.32957, 0.33556, 0.3311, 0.32631, 0.32217],
    [0.34959, 0.34196, 0.33573, 0.32961, 0.3361, 0.33176, 0.32704, 0.32296],
    [0.34934, 0.34181, 0.33561, 0.32964, 0.33658, 0.33235, 0.32769, 0.32368],
    [0.34912, 0.34167, 0.3355, 0.32967, 0.33701, 0.33288, 0.32827, 0.32432],
    [0.34891, 0.34154, 0.33539, 0.3297, 0.33742, 0.33337, 0.32881, 0.32492]]

class TestHeston(unittest.TestCase):
    def test_heston(self):
        black = heston.black_surface(calculation_date, expiration_dates, strikes, iv)
        assert black.blackVol(1.2, 600) >= 0.3
        hes = heston.heston_surface(calculation_date, spot, expiration_dates, strikes, iv)
        assert hes.blackVol(1.2, 600) >= 0.3

        test_res = {}
        expiry = [day_count.yearFraction(calculation_date, d) for d in expiration_dates]
        test_res['actual'] = pd.DataFrame(iv, index=expiry, columns=strikes)

        extrapolate_expiry = np.linspace(0.1, max(expiry), 100)

        black_iv = [[black.blackVol(ex, s) for s in strikes]
                    for ex in extrapolate_expiry]
        test_res['black'] = pd.DataFrame(
            black_iv, index=extrapolate_expiry, columns=strikes)

        print(colored('Black Model Fitted IV', 'green'))
        print(test_res['black'].to_markdown())

        heston_iv = [[hes.blackVol(ex, s) for s in strikes]
                     for ex in extrapolate_expiry]
        test_res['heston'] = pd.DataFrame(
            heston_iv, index=extrapolate_expiry, columns=strikes)

        print(colored('Heston Model Fitted IV', 'green'))
        print(test_res['heston'].to_markdown())

        with pd.ExcelWriter('test.xlsx') as w:
            for model_name, value in test_res.items():
                value.to_excel(w, model_name)
        
        surf = utils.plot_vol_surface(strikes, extrapolate_expiry, black_iv)
        surf.savefig('test_vol_surface_black.png')

        surf = utils.plot_vol_surface(strikes, extrapolate_expiry, heston_iv)
        surf.savefig('test_vol_surface_heston.png')

    def test_utils(self):
        fig = utils.plot_vol_smile(strikes, iv[0])
        fig.savefig('test_vol_smile.png')
        expiry = [day_count.yearFraction(calculation_date, d) for d in expiration_dates]
        surf = utils.plot_vol_surface(strikes, expiry, iv)
        surf.savefig('test_vol_surface_raw.png')
        