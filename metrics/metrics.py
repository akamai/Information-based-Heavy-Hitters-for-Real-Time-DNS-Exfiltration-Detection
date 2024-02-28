def true_positive_rate(tp, fn):
    return tp / (tp + fn)


def false_positive_rate(fp, tn):
    return fp / (fp + tn)
