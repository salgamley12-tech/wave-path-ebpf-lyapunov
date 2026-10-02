from lyapunov.lyapunov import LyapunovResult


def wave_row_to_lyapunov(row) -> LyapunovResult:
    if len(row) < 5:
        raise ValueError("wave row must contain t, u, v, V, dVdt")

    return LyapunovResult(
        V=float(row[3]),
        dVdt=float(row[4]),
    )


def wave_rows_to_lyapunov(rows):
    return [wave_row_to_lyapunov(row) for row in rows]
