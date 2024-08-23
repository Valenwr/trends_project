from pytrends.request import TrendReq
import pandas as pd

def normalize_with_reference(df, reference):
    """
    Normalize dataframe values with respect to a reference column.
    
    Args:
    df (pandas.DataFrame): Input dataframe.
    reference (str): Name of the reference column.
    
    Returns:
    pandas.DataFrame: Normalized dataframe.
    """
    reference_values = df[reference]
    return df.div(reference_values, axis=0) * 100

def get_trends_data_with_reference(keywords, reference, period='today 5-y', geo=''):
    """
    Fetch Google Trends data for multiple keywords and normalize with respect to a reference keyword.
    
    Args:
    keywords (list): List of keywords to analyze.
    reference (str): Reference keyword for normalization.
    period (str): Time period for analysis. Default is 'today 5-y'.
    geo (str): Geographic location for the trends. Default is '' (worldwide).
    
    Returns:
    pandas.DataFrame: Normalized trends data.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    all_data = pd.DataFrame()

    # Process keywords in batches of 4 (Google Trends limitation)
    for i in range(0, len(keywords), 4):
        batch_keywords = keywords[i:i + 4]
        batch_keywords.append(reference)
        pytrends.build_payload(batch_keywords, cat=0, timeframe=period, geo=geo, gprop='')
        data = pytrends.interest_over_time()
        
        normalized_data = normalize_with_reference(data, reference)
        
        if all_data.empty:
            all_data = normalized_data
        else:
            all_data = pd.concat([all_data, normalized_data], axis=1)

    return all_data.drop(columns=[reference])

def get_individual_data_with_reference(keywords, reference, period='today 5-y', geo=''):
    """
    Fetch Google Trends data for individual keywords compared to a reference keyword.
    
    Args:
    keywords (list): List of keywords to analyze.
    reference (str): Reference keyword for comparison.
    period (str): Time period for analysis. Default is 'today 5-y'.
    geo (str): Geographic location for the trends. Default is '' (worldwide).
    
    Returns:
    pandas.DataFrame: Trends data for individual keywords and reference.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    all_data = pd.DataFrame()

    for keyword in keywords:
        batch_keywords = [keyword, reference]
        pytrends.build_payload(batch_keywords, cat=0, timeframe=period, geo=geo, gprop='')
        data = pytrends.interest_over_time().drop(columns=['isPartial'])
        
        if all_data.empty:
            all_data = data
        else:
            all_data = pd.concat([all_data, data[keyword]], axis=1)

    return all_data

