def predict_next_number(prices: list[float]) -> float:
    """
    Predicts the next gold futures price from a given sequence of historical values.
    
    The prediction is adjusted dynamically using an optimal shift to satisfy 
    asymmetric tolerances:
    - Within 1 if the predicted next number is lower than actual.
    - Within 10 if the predicted next number is higher than actual.
    
    Args:
        prices (list[float]): A list of up to 100 historical gold prices.
        
    Returns:
        float: The predicted next price, rounded to two decimal places.
    """
    if not prices:
        return 0.0
    n = len(prices)
    if n == 1:
        return prices[0]

    def get_base_prediction(series: list[float], w: int) -> float:
        """Fits a local linear regression on the last 'w' points to predict the next."""
        if len(series) < w:
            w = len(series)
        if w <= 1:
            return series[-1] if series else 0.0
        
        y = series[-w:]
        x = list(range(1, w + 1))
        mean_x = (w + 1) / 2.0
        mean_y = sum(y) / float(w)
        
        var_x = sum((xi - mean_x) ** 2 for xi in x)
        if var_x == 0:
            return y[-1]
            
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(w))
        slope = cov_xy / var_x
        intercept = mean_y - slope * mean_x
        
        return slope * (w + 1) + intercept

    # Grid search over candidate parameters to find the most stable local fit.
    # We evaluate window sizes 'w' and historical evaluation lengths 'M'.
    best_w = 3
    best_M = 8
    min_range = float('inf')
    best_errors = []
    
    w_candidates = [1, 2, 3, 4, 5, 6, 8]
    M_candidates = [5, 8, 10, 12, 15, 20]
    
    for w in w_candidates:
        for M in M_candidates:
            start_t = max(w, n - M)
            # Ensure we have at least 3 historical points to evaluate the range
            if n - start_t < 3:
                continue
                
            errors = []
            for t in range(start_t, n):
                pred = get_base_prediction(prices[:t], w)
                errors.append(prices[t] - pred)
                
            e_range = max(errors) - min(errors)
            if e_range < min_range:
                min_range = e_range
                best_w = w
                best_M = M
                best_errors = errors

    # Calculate the base prediction for the next step
    next_base_pred = get_base_prediction(prices, best_w)
    
    # Calculate the optimal shift C based on historical errors
    if best_errors:
        e_max = max(best_errors)
        e_min = min(best_errors)
        C = (e_max + e_min) / 2.0 - 4.5
    else:
        C = 4.5  # Default shift if historical data is too limited

    prediction = next_base_pred + C
    return round(prediction, 2)