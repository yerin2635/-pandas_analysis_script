def calculate_cost(usage, metrics: list, pricings: list):
    total = 0
    metrics.reverse()
    pricings.reverse()

    for i, metric in enumerate(metrics):

        if usage < metric:
            continue

        consume = usage - metric
        total += consume * pricings[i]
        usage -= consume

    return total
