import json
import urllib
import pandas as pd
import copy

def fetch_oecd_data(idd_base_url = 'http://stats.oecd.org/sdmx-json/data/IDD',
                    dimension_filter = 'all', # grab all data
                    time_filter = 'all?startTime=2001&endTime=2014',
                    optional_filters = '&detail=dataonly'):

    data_query = idd_base_url + '/' + dimension_filter + '/' + time_filter + optional_filters
    stats_oecd_idd = json.load(urllib.urlopen(data_query))

    """parse json data into DataFrame:

    the json comes with a 'structure' section which explains how to
    interpret the keys (e.g. 1:2:3:4:5) for the observations.

    We first need to parse the 'structure' to figure out what the
    dimension names (and order) is. Then, we need to unpack
    observation values into floats (as opposed to arrays)
    """
    metadata_stats_oecd_idd = stats_oecd_idd['structure']['dimensions']

    col_names = []
    for dim in metadata_stats_oecd_idd['series']:
        col_names.append(dim['id'].lower())

    idd_dataframe = pd.DataFrame()

    for key, value in stats_oecd_idd['dataSets'][0]['series'].items():

        data = pd.DataFrame(dict(zip(col_names, [[x] for x in key.split(":")])))

        observations = copy.copy(value['observations'])

        for time, measure in observations.items():
            observations[time] = measure[0]

        observations = pd.DataFrame(observations.items(), columns=['time_period','observation'])

        observations['location'] = data['location'].iloc[0]

        data = pd.merge(right=data,\
                        left=observations,\
                        on='location',\
                        how='outer')

        idd_dataframe = idd_dataframe.append(data, ignore_index=False)
        
    return idd_dataframe, metadata_stats_oecd_idd

def append_metadata_to_oecd_stats(idd_dataframe, metadata_stats_oecd_idd):
    """
    Append meta data to OECD stats dataframe:

    the returned JSON has a 'structure' object with 'dimensions'
    child that contains all the information to translate series
    identifiers x:y:z:w:a into something human parsable.

    A series of merges should be anticipated. Hence, it makes
    sense to store all the metadata in a dictionary where the
    keys will be the merge indices.
    """
    oecd_metadata = {}
    for dim in metadata_stats_oecd_idd['series']:
        dim_dataframe = pd.DataFrame(dim['values'])
        dim_id = dim['id'].lower()
        dim_dataframe.columns = [dim_id + '_code', dim_id + '_name']
        dim_dataframe[dim_id] = dim_dataframe.index.astype(str)
        oecd_metadata[dim_id] = dim_dataframe

    # make time metadata
    time_metadata = metadata_stats_oecd_idd['observation'][0]
    time_metadata_index = time_metadata['role'].lower()
    time_metadata_df = pd.DataFrame(time_metadata['values'])
    time_metadata_df.columns = ['year', time_metadata_index]
    time_metadata_df[time_metadata_index] = time_metadata_df.index.astype(str)

    oecd_metadata[time_metadata_index] = time_metadata_df

    for key, df in oecd_metadata.items():
        idd_dataframe = pd.merge(left=idd_dataframe,\
                                 right=df,\
                                 how='left',\
                                 on=key)
    return idd_dataframe

def fetch_and_format_oecd_data(idd_base_url = 'http://stats.oecd.org/sdmx-json/data/IDD',
                               dimension_filter = 'all', # grab all data
                               time_filter = 'all?startTime=2001&endTime=2014',
                               optional_filters = '&detail=dataonly'):
    return append_metadata_to_oecd_stats(*fetch_oecd_data(idd_base_url, dimension_filter, time_filter, optional_filters))