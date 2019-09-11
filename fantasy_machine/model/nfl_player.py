import numpy as np
import pandas as pd
import scipy.stats as st


def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

def filter_data(name=slice(None), year=slice(None), week=slice(None), 
                team=slice(None), position=slice(None), opponent=slice(None)):
    in_pos = df_g.loc[(name, year, week, team, position, opponent),:]
    data = in_pos['f_score']

    return data

def make_prediction(feature_set, dist_=st.gengamma, plot=False, readout=False):
    """Takes a set of features in the form of prefious data and generates an aggreagated
    p"""
    cum_rvs = np.array([])
    for pred_feature in feature_set:
        p_fit = dist_.fit(pred_feature['payload'])
        p_vals = dist_.rvs(*p_fit[:-2], loc=p_fit[-2], scale=p_fit[-1], size=10000)
        cum_rvs = np.concatenate((p_vals, cum_rvs))
        pred_feature['pdf'] = make_pdf(dist_, p_fit, size=10000)
    
    pm_p = dist_.fit(cum_rvs)
    feature_set.append({'label':'Prediction','pdf':make_pdf(dist_, pm_p, size=10000)})
    
    if plot:
        plot_feature_pred(feature_set)

    if readout:
        prediction_topline_readout(predictor_params=pm_p, dist=dist_)
        
    return pm_p
    
def prediction_topline_readout(predictor_params, dist):
    _25 = round(dist.ppf(0.25, *pm_p),2)
    _50 = round(dist.ppf(0.5, *pm_p),2)
    _75 = round(dist.ppf(0.75, *pm_p),2)
    _25_50 = int((_50-_25)/_50*100)
    _75_50 = int((_75-_50)/_50*100)

    pred_string = f"""
    Pred Points: {_50}
    Lower Bound: {_25} [{_25_50}%]
    Upper Bound: {_75} [{_75_50}%]
    """
    print(pred_string)
 
def plot_feature_pred(feature_set):
    fig, ax1 = plt.subplots(1,1, figsize=(10,6), dpi=200)
    ax2 = ax1.twinx()
    for feature in feature_set:
        plot_arg = {'ls':'--','lw':2.0, 'color':'black'} if feature['label'] == 'Prediction' else {'ls':'-'}
        ax1.plot(feature['pdf'].index, 
             feature['pdf'].values, 
             label=feature['label'],
             **plot_arg)
        try:
             ax2.hist(feature['payload'], 
             bins=20, 
             alpha=.1,
             label=feature['label'])
        except:
            pass
    ax1.legend(loc=1)
    ax2.legend(loc=5)