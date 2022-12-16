import QuantLib as ql

def get_day_count():
    return ql.Actual365Fixed()

def get_calendar():
    return ql.China()

def _convert_to_qlMatrix_transpose(matrix):
    # return matrix.T as ql.Matrix, which is required in surface building.
    ql_mat = ql.Matrix(len(matrix[0]), len(matrix))
    for i in range(ql_mat.rows()):
        for j in range(ql_mat.columns()):
            ql_mat[i][j] = matrix[j][i]
    return ql_mat

def black_surface(calculation_date: ql.Date, 
                  expiration_dates: [ql.Date], 
                  strikes: [float], 
                  iv: [[float]]):
    # IV should be a matrix indexed by (expiration_date, strike).
    # Each row should be the IV of different strike on the same expiry.

    assert len(iv) == len(expiration_dates), 'iv and expiratiton_dates shape mis-match'
    assert len(iv[0]) == len(strikes), 'iv and strikes shape mis-match'

    implied_vols = _convert_to_qlMatrix_transpose(iv)
    day_count = get_day_count()
    calendar = get_calendar()

    black_var_surface = ql.BlackVarianceSurface(
        calculation_date, calendar,
        expiration_dates, strikes,
        implied_vols, day_count)

    return black_var_surface


def heston_surface(calculation_date: ql.Date,
                   spot: float,
                   expiration_dates: [ql.Date],
                   strikes: [float],
                   iv: [[float]]):
    # In Heston, spot is needed.
    # IV should be a matrix indexed by (expiration_date, strike).
    # Each row should be the IV of different strike on the same expiry.
    assert len(iv) == len(expiration_dates), 'iv and expiratiton_dates shape mis-match'
    assert len(iv[0]) == len(strikes), 'iv and strikes shape mis-match'

    day_count = get_day_count()
    calendar = get_calendar()

    # Dummy variables, will be overwritten in model calibration.
    v0 = 0.01
    kappa = 0.01
    theta = 0.01
    rho = 0.0
    sigma = 0.01

    riskFreeCurve = ql.FlatForward(calculation_date, 0.0, day_count)
    flat_ts = ql.YieldTermStructureHandle(riskFreeCurve)
    dividend_ts = ql.YieldTermStructureHandle(riskFreeCurve)

    process = ql.HestonProcess(flat_ts, dividend_ts,
                               ql.QuoteHandle(ql.SimpleQuote(spot)),
                               v0, kappa, theta, sigma, rho)
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)

    heston_helpers = []

    for s, date, ivs in zip(strikes, expiration_dates, iv):
        t = (date - calculation_date)
        p = ql.Period(t, ql.Days)
        for sigma in ivs:
            helper = ql.HestonModelHelper(p, calendar, spot, s,
                                          ql.QuoteHandle(ql.SimpleQuote(sigma)),
                                          flat_ts,
                                          dividend_ts)
            helper.setPricingEngine(engine)
            heston_helpers.append(helper)

    lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
    model.calibrate(heston_helpers, lm,
                    ql.EndCriteria(50000, 50, 1.0e-8, 1.0e-8, 1.0e-8))
                    
    heston_handle = ql.HestonModelHandle(model)
    heston_vol_surface = ql.HestonBlackVolSurface(heston_handle)

    return heston_vol_surface
