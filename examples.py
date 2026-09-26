"""Built-in teaching examples; treated as read-only specifications."""

EXAMPLES = {
    'AR(1): persistent': {
        'p': 1,
        'q': 0,
        'ar': [0.8],
        'ma': [],
    },

    'AR(1): random walk': {
        'p': 1,
        'q': 0,
        'ar': [1.0],
        'ma': [],
    },

    'AR(1): explosive': {
        'p': 1,
        'q': 0,
        'ar': [1.2],
        'ma': [],
    },

    'AR(2): oscillatory': {
        'p': 2,
        'q': 0,
        'ar': [1.2, -0.8],
        'ma': [],
    },

    'MA(1)': {
        'p': 0,
        'q': 1,
        'ar': [],
        'ma': [0.5],
    },

    'MA(1): non-invertible': {
        'p': 0,
        'q': 1,
        'ar': [],
        'ma': [1.5],
    },

    'ARMA(1,1)': {
        'p': 1,
        'q': 1,
        'ar': [0.8],
        'ma': [0.5],
    },

    'Common root': {
        'p': 1,
        'q': 1,
        'ar': [0.5],
        'ma': [-0.5],
    },

    'ARMA(2,1): complex AR roots': {
        'p': 2,
        'q': 1,
        'ar': [1.2, -0.8],
        'ma': [0.5],
    },
}
