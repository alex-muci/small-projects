""" My own formula as derived around Sept-Oct 2020  """
import collections
import numpy as np
from scipy.stats import norm

import tensorflow as tf
# import tensorflow_probability as tfp
# tfd = tfp.distributions
N = norm.cdf
RES = collections.namedtuple('RES', ['price', 'delta', 'gamma', 'vega', 'theta'])


#  ###############################################   ################################################
#  TENSORFLOW VERSION
#  ###############################################   ################################################
# @tf.function  # <----- NB: static graph not possible since matrix shapes depend on data (weights > nd < 0)
def basket_approx_tf(opt_type: str, T: float, r: float, strike: float,
                     fwds, sigmas, correls, weights=None, dtype=tf.float64,
                     greeks=False):
    """
    Basket (and spread) general approximation
    assuming a log-normal distribution for each underlying futures:

    > Tensorflow implementation with AutoDiff Greeks
    >> NB: static graph not possible since matrix shapes depend on data  <<

     call_payoff = max(Sum_i^L w_i fwd_i - Sum_j^S w_j fwd_j - strike, 0.)
                   where there are L long fwds and N short fwds
     put_payoff  = max(strike - (Sum_i^L w_i fwd_i - Sum_j^S w_j fwd_j), 0.)   by put-call parity

     i.e. the formula incorporates spread options, e.g. crack clean spread options by setting L=1 and S=2.

    :param opt_type: 'c' or 'p'
    :param T: time to expiry in years (e.g. 0.5 for 6 months)
    :param r: interest rate
    :param strike: strike of the option (>0)
    :param fwds: list of all current forward prices
    :param sigmas: list of volatilities for the forwards returns
    :param correls: correlation matrix
    :param weights: list of weights (positive for long assets, negative for short assets), default = equally weighted
    :param dtype (Optional): float64
    :param greeks (Optional): either price (if greeks=False, default) or price with Greeks (if greeks=True)

    :return: lognormal model basket (and spread) prices and Greeks (if greeks=True)
            if greeks = True
                (i) single values as: call.price, call.delta, call.gamma, call.vega, call.theta
                (ii) all values as tuple: call._asdict().values()
            if greeks = False
                return single value

    # SPREAD Example
    T = 1
    r = 0.05
    strike = 30  # ATM
    fwds = [100, 24, 46]
    sigmas = [0.4, 0.22, 0.3]
    r12, r13, r23 = 0.91, 0.91, 0.43
    correls = [[1., r12, r13], [r12, 1, r23], [r13, r23, 1.]]
    weights = [1, -1., -1.]

    OR

    # BASKET Example
    T  = 5  # 5 years
    r = 0.
    fwds = 100. * np.ones(4)
    sigmas = 0.4 * np.ones(4)
    correls = 0.5 * np.ones((4, 4))
    np.fill_diagonal(correls, 1.)
    weights = 0.25 * np.ones(4)
    strikes = 100

    # A. if greeks=False (which is the default value):
    call_price = basket_approx_tf(opt_type='c', T=T, r=r, strike=k_i,
                                  fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)

    # B. if greeks=True:
    call = basket_approx_tf(opt_type='c', T=T, r=r, strike=k_i, greeks=True,
                            fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
        (i) single values as: call.price, call.delta, call.gamma, call.vega, call.theta
        (ii) all values as tuple: call._asdict().values()
    """
    # get type conversion (for consistency and to avoid inputs errors)
    if opt_type.lower() not in ('c', 'p'): raise ValueError("select either 'c' (call) or 'p' (put) -tertium non datum.")
    opt_type = tf.constant(opt_type.lower(), dtype=tf.string)
    T, r, strike = tf.convert_to_tensor(T, dtype), tf.constant(r, dtype), tf.constant(strike, dtype)
    fwds = tf.convert_to_tensor(fwds, dtype)
    sigmas = tf.convert_to_tensor(sigmas, dtype)
    correls = tf.convert_to_tensor(correls, dtype)
    w = tf.ones(fwds.shape[0], dtype=dtype) / fwds.shape[0] if weights is None else tf.convert_to_tensor(weights, dtype)

    ###################################################################################################################
    # noinspection PyShadowingNames
    def bkt_price(opt_type, T, r, strike, fwds, sigmas, correls, w):
        zero, one = tf.constant(0, dtype), tf.constant(1, dtype)
        sigmas_v = tf.expand_dims(sigmas, -1)  # (no_vols ,) -> (no_vols, 1)
        cov_matrix = sigmas_v * correls * tf.transpose(sigmas_v)  # elemnt-wise (slightly faster) than below dot product
        # diag_vol = tf.linalg.diag(sigmas);cov_matrix = tf.linalg.matmul(tf.linalg.matmul(diag_vol, correls), diag_vol)

        # split arrays: L long from S short
        long = tf.greater(w, 0.)  # w > 0  # vs. short = tf.math.logical_not(long)
        w_l, w_s = tf.boolean_mask(w, long), tf.math.abs(tf.boolean_mask(w, ~long))  # w[long], np.abs(w[~long])
        L, S = w_l.shape[0], w_s.shape[0]
        fwds_l, fwds_s = tf.boolean_mask(fwds, long), tf.boolean_mask(fwds, ~long)   # fwds[long], fwds[~long]

        cov_mat_ord1 = tf.concat((cov_matrix[long], cov_matrix[~long]), axis=0)  # order rows
        l = tf.boolean_mask(tf.range(cov_mat_ord1.shape[1]), long)
        s = tf.boolean_mask(tf.range(cov_mat_ord1.shape[1]), ~long)  # order cols
        cov_mat_ord = tf.concat((tf.gather(cov_mat_ord1, l, axis=1), tf.gather(cov_mat_ord1, s, axis=1)), axis=1)

        # pre-computed vars
        b_l, b_s = w_l * fwds_l, w_s * fwds_s
        e_F, e_K = tf.math.reduce_sum(b_l), (tf.math.reduce_sum(b_s) + strike)
        b_l, b_s = b_l / e_F, b_s / e_K

        df = tf.math.exp(-r * T) # by default dtype=np.float64
        T_sqrt = tf.math.sqrt(T)

        # calculate volatility
        b_ord = tf.concat((b_l, -b_s), axis=0)  # NB: only for shape (n,) use numpy hstack but tf vstack (axis=0)
        var = tf.tensordot(b_ord, tf.tensordot(cov_mat_ord, b_ord, 1),1)
        vol = tf.math.sqrt(var)

        # calculate d_k
        long_var = tf.tensordot(b_l, tf.tensordot(cov_mat_ord[:L, :L], b_l, 1),1)
        short_var = tf.tensordot(b_s, tf.tensordot(cov_mat_ord[L:, L:], b_s, 1),1)
        d_k = (tf.math.log(e_F) - tf.math.log(e_K) - 0.5 * (long_var - short_var) * T) / (vol * T_sqrt)

        # calculate d_fwds
        d_fwds = (tf.tensordot(cov_mat_ord[:, :L], b_l, 1) -
                  tf.tensordot(cov_mat_ord[:, L:], b_s, 1)) * T_sqrt / vol + d_k

        norm = tfd.Normal(loc=zero, scale=one)
        long_value = tf.math.reduce_sum(w_l[:L] * fwds_l[:L] * norm.cdf(d_fwds[:L]))
        short_value = tf.where(tf.equal(S, 0), zero,
                               tf.math.reduce_sum(w_s[:S] * fwds_s[:S] * norm.cdf(d_fwds[L:L + S])))
        # intrinsic = np.sum(fwds * w) - strike * df

        call = df * (long_value - short_value - strike * norm.cdf(d_k))
        call = tf.math.maximum(0., call)  # np.maximum(np.maximum(intrinsic, 0.), call)

        res = tf.where(opt_type == 'c', call,
                       tf.math.maximum(0., call - (tf.math.reduce_sum(fwds * w) - strike) * df ))
        return res

    ###################################################################################################################

    if not greeks:  # then just return the price
        return bkt_price(opt_type, T, r, strike, fwds, sigmas, correls, w)

    # calculate the Greeks -> then return price and Greeks
    with tf.GradientTape() as outer_tape:
        outer_tape.watch(fwds)
        with tf.GradientTape() as in_tape:
            in_tape.watch(fwds)
            in_tape.watch(sigmas)
            in_tape.watch(T)
            # in_tape.watch(r)
            price = bkt_price(opt_type, T, r, strike, fwds, sigmas, correls, w)
        delta, vega, theta = in_tape.gradient(price, [fwds, sigmas, T], unconnected_gradients='zero')
    gamma = outer_tape.gradient(delta, [fwds])[0]

    return RES(price, delta, gamma, vega * 0.01, theta * -1. / 365.)  # res._asdict().values()


#  ###############################################   ################################################
#  NUMPY VERSION
#  ###############################################   ################################################
def basket_approx_py(opt_type: str, T: float, r: float, strike: float,
                     fwds, sigmas, correls, weights=None, dtype=np.float64):  # sigmas: np.ndarray
    """
    Basket (and spread) general approximation
    assuming a lognormal distribution for each underlying futures:

    > Numpy implementation (price only, for Greeks use the Tensorflow implementation: basket_approx_tf()

     call_payoff = max(Sum_i^L w_i fwd_i - Sum_j^S w_j fwd_j - strike, 0.)
                   where there are L long fwds and N short fwds
     put_payoff  = max(strike - (Sum_i^L w_i fwd_i - Sum_j^S w_j fwd_j), 0.)   by put-call parity

     i.e. the formula incorporates spread options, e.g. crack clean spread options by setting L=1 and S=2.

    :param opt_type: 'c' or 'p'
    :param T: time to expiry in years (e.g. 0.5 for 6 months)
    :param r: interest rate
    :param strike: strike of the option (>0)
    :param fwds: list of all current forward prices
    :param sigmas: list of volatilities for the forwards returns
    :param correls: correlation matrix
    :param weights: list of weights (positive for long assets, negative for short assets), default = equally weighted
    :param dtype (Optional): float64

    :return: lognormal model basket (and spread) prices

    # SPREAD Example
    T = 1
    r = 0.05
    strike = 30  # ATM
    fwds = [100, 24, 46]
    sigmas = [0.4, 0.22, 0.3]
    r12, r13, r23 = 0.91, 0.91, 0.43
    correls = [[1., r12, r13], [r12, 1, r23], [r13, r23, 1.]]
    weights = [1, -1., -1.]

    OR

    # BASKET Example
    T  = 5  # 5 years
    r = 0.
    fwds = 100. * np.ones(4)
    sigmas = 0.4 * np.ones(4)
    correls = 0.5 * np.ones((4, 4))
    np.fill_diagonal(correls, 1.)
    weights = 0.25 * np.ones(4)
    strikes = 100

    call = basket_approx_py(opt_type='c', T=T, r=r, strike=k_i,
                            fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
    """
    # 1. transform and order inputs
    fwds = np.array(fwds, dtype=dtype)
    sigmas = np.array(sigmas, dtype=dtype)
    correls = np.array(correls, dtype=dtype)
    w = np.ones(fwds.shape[0], dtype=dtype)/fwds.shape[0] if (weights is None) else np.array(weights, dtype=dtype)

    diag_vol = np.diag(sigmas)
    correl_np = np.array(correls)
    cov_matrix = np.dot(np.dot(diag_vol, correl_np), diag_vol)

    # split arrays: L long from S short
    long = w > 0
    w_l, w_s = w[long], np.abs(w[~long])
    L, S = w_l.shape[0], w_s.shape[0]
    fwds_l, fwds_s = fwds[long], fwds[~long]

    cov_mat_ord1 = np.vstack((cov_matrix[long], cov_matrix[~long]))  # order rows
    cov_mat_ord = np.hstack((cov_mat_ord1[:, long], cov_mat_ord1[:, ~long]))  # order cols

    # pre-computed vars
    b_l, b_s = w_l * fwds_l, w_s * fwds_s
    e_F, e_K = np.sum(b_l), (np.sum(b_s) + strike)
    b_l, b_s = b_l / e_F, b_s / e_K

    df = np.exp(-r * T)  # by default dtype=np.float64
    T_sqrt = np.sqrt(T)

    # calculate volatility
    b_ord = np.hstack((b_l, -b_s))  # NB: minus
    var = np.dot(np.dot(b_ord, cov_mat_ord), b_ord)
    vol = np.sqrt(var)

    # calculate d_k
    long_var = np.dot(np.dot(b_l, cov_mat_ord[:L, :L]), b_l)
    short_var = np.dot(np.dot(b_s, cov_mat_ord[L:, L:]), b_s)
    d_k = (np.log(e_F) - np.log(e_K) - 0.5 * (long_var - short_var) * T) / (vol * T_sqrt)

    # calculate d_fwds
    d_fwds = (np.dot(cov_mat_ord[:, :L], b_l) - np.dot(cov_mat_ord[:, L:], b_s)) * T_sqrt / vol + d_k

    long_value = np.sum(w_l[:L] * fwds_l[:L] * N(d_fwds[:L]))
    short_value = np.sum(w_s[:S] * fwds_s[:S] * N(d_fwds[L:L+S]))
    # intrinsic = np.sum(fwds * w) - strike * df

    call = df * (long_value - short_value - strike * N(d_k))
    call = np.maximum(0., call)  # np.maximum(np.maximum(intrinsic, 0.), call)

    if opt_type.lower() == 'c':
        return call
    elif opt_type.lower() == 'p':
        put = call - (np.sum(fwds * w) - strike) * df  # by put-call parity
        return np.maximum(0., put)  # np.maximum(np.maximum(-intrinsic, 0.), put)
    else:
        raise ValueError("select either 'c' (call) or 'p' (put) - tertium non datum.")


# #############################################################################
if __name__ == '__main__':

    T = 5.  # 5 years
    r = 0.
    fwds = 100. * np.ones(4)
    sigmas = 0.4 * np.ones(4)
    correls = 0.5 * np.ones((4, 4))
    np.fill_diagonal(correls, 1.)
    weights = None  # 0.25 * np.ones(4)

    strikes = [80, 100, 120]
    expected_calls = [36.04, 27.63, 21.36]  # lower bounds from paper vs. simulated 36.35, 28.00, 21.76 from paper

    for i, k_i in enumerate(strikes):
        call = basket_approx_py(opt_type='c', T=T, r=r, strike=k_i,
                                fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
        print(round(call, 2), expected_calls[i])

    """
    for i, k_i in enumerate(strikes):
        call = basket_approx_tf(opt_type='c', T=T, r=r, strike=k_i,
                                fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
        print(round(call.numpy(), 2), expected_calls[i])
        

    # #########################################################################
    weights = [-0.25, -0.25, 0.25, 0.25]
    fwds = [6, 3, 4, 5]
    sigmas = [0.5, 0.5, 0.3, 0.2]

    call_greeks = basket_approx_tf(opt_type='c', T=T, r=r, strike=4, greeks=True,
                                   fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
    print(call_greeks.price.numpy(), '\n',
          call_greeks.delta.numpy(), '\n',
          call_greeks.gamma.numpy(), '\n',
          call_greeks.vega.numpy(),  '\n',
          call_greeks.theta.numpy())

    # ##################################
    perm = [2, 3, 0, 1]
    weights, fwds, sigmas = np.array(weights), np.array(fwds), np.array(sigmas)
    fwds, sigmas, weights = fwds[perm], sigmas[perm], weights[perm]

    call_greeks = basket_approx_tf(opt_type='c', T=T, r=r, strike=4, greeks=True,
                                   fwds=fwds, sigmas=sigmas, correls=correls, weights=weights, dtype=np.float64)
    print(call_greeks.price.numpy(), '\n',
          call_greeks.delta.numpy(), '\n',
          call_greeks.gamma.numpy(), '\n',
          call_greeks.vega.numpy())
    """
