import QuantLib as ql

def get_day_count():
    return ql.Actual365Fixed()

def get_calendar():
    return ql.China()

def _convert_to_qlMatrix_transpose(matrix):
    # return matrix.T as ql.Matrix.
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

def heston_surface(expiration_dates: [ql.Date],strikes: [float], iv:[[float]]):
    pass
