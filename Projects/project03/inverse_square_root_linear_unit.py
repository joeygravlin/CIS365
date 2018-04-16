import math


# IInverse Square Root Linear Unit (ISRLU)
# https://arxiv.org/pdf/1710.09967.pdf
def isrlu(x):
    # , alpha=None):
    # alpha = None
    # if x >= 0:
    #     return x
    # else:
    if x < 0:
        # if alpha is None:
        alpha = 1
        ret = x/math.sqrt(1+alpha*(x**2))
    else:
        ret = x
    return ret


# config.genome_config.add_activation('inverse_square_root_linear_unit', isrlu)
