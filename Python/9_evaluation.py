from sklearn.metrics import f1_score

def evaluation(y_pred, y_true):
    """ This function evaluates the model calculating the weighted f1-score based
    on the inputs `y_pred` (predictions by the model) and `y_true` (actual values). 
    
    Parameters
    ----------
    y_pred: list or np.array
        This parameter stores the predicted classes.

    y_true: list or np.array
        This parameter stores the actual classes (true values).

    Returns
    -------
    This function returns weighted f1-score.
    """
    weighted_f1_score = f1_score(y_true, y_pred, average='weighted')
    
    return weighted_f1_score 
