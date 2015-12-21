import json
import urllib.request
import pandas as pd
import copy


def fetch_and_reshape_oecd_json(data_code,
                                dimension_filter='all',
                                time_and_other_filters='all?detail=Full'):
    """
    Pull down and reshape a specific data set from stats.oecd.org

    the stats.oecd.org api [documentation](https://data.oecd.org/api/sdmx-json-documentation/)
    outlines the taxonomy of a data request as:

    stats.oecd.org/sdmx-json/data/datasetcode/dimension_filter/time_and_other_filters

    E.g., say
    * we want the "Growth in GDP per capita, productivity and ULC" data
        + the data code is PDB_GR
    * we want stats for Australia and USA
        + their location codes are AUS, USA
    * we're interested in "GDP per capita, constant prices", and "GDP per hour worked, constant prices"
        + their measure codes are T_GDPPOP_V, T_GDPHRS_
    * and we want to look at these measures through the perspectives of
        + a valued indexed according to measure at 2010
            - this has attribute code 2010Y
        + Annual growth/change,
            - this has attribute code GR
        + Average growth rate
            - this has attribute code AVGRW
    * we want all data between 1970 and 2014
        + we can use the filter "all?startTime=1970&endTime=2014"
    * we want the full detail of the data:
        + append "&detail=Full" to our time filter

    According to the API, we separate dimension and other filters by "/", and
    inside the dimension filter we concatenate with "+" and separate with ".".
    Hence, our request would look like:

    http://stats.oecd.org/sdmx-json/data/PDB_GR/AUS+USA.T_GDPPOP_V+T_GDPHRS_V.2010Y+GRW+AVGRW/all?startTime=1970&endTime=2014&detail=Full

    If we just want to grab all data, and filter later (I highly suggest this):

    http://stats.oecd.org/sdmx-json/data/PDB_GR/all/all?detail=Full

    Unfortunately, the way the data is setup, your data comes back as in JSON format,
    but the dataset spec is in XML and can be accessed via

    http://stats.oecd.org/restsdmx/sdmx.ashx/GetDataStructure/datasetcode

    For reshaping the data, the XML isn't necessary -- just fetch the data with "detail=Full"
    in the request.

    :param data_code: a string indicating the stats.oecd.org data set to be fetched.
    :param dimension_filter: a string conforming to
       [the stats.oecd.org api documentation](https://data.oecd.org/api/sdmx-json-documentation/)
       indicating how dimensions should be filtered. See function description.
    :param time_and_other_filters: a string conforming to the stats.oecd.org api that indicates
        how the time (and detail) dimensions should be filtered. See function description

    :returns: a pandas DataFrame.

    Example input for a request for Income Disparity Data:

    idd_base_url = 'http://stats.oecd.org/sdmx-json/data/IDD'
    dimension_filter = 'all' # grab all data
    time_filter = 'all?startTime=2001&endTime=2014'
    optional_filters = '&detail=Full' # pick up the measure unit's...
    """

    """parse json data into DataFrame:

    the json comes with a 'structure' section which explains how to
    interpret the keys (e.g. 1:2:3:4:5) for the observations.

    We first need to parse the 'structure' to figure out what the
    dimension names (and order) is. Then, we need to unpack
    observation values into floats (as opposed to arrays)
    """
    idd_base_url = "http://stats.oecd.org/sdmx-json/data"
    data_query = idd_base_url + '/' + data_code + '/' + dimension_filter + '/' + time_and_other_filters
    stats_oecd_idd = json.loads(urllib.request.urlopen(data_query).read().decode('utf-8'))

    """
    stats_oecd_idd is a dictionary with keys:
        + structure -- a dict with keys ['annotations', 'attributes', 'dimensions', 'links', 'name', 'description'].
        These keys hold dictionaries as values, whose keys yield further information about the data structure. E.g.:
            - attributes yields a dict with keys ['dataSet', 'observation', 'series']
            - dimensions yields a dict with keys ['observation', 'series']
        Hence, structure.attributes.series contains information about the series' attributes, and
        structure.dimensions.observation yields information about the dimension of observations.
        + dataSets -- a list containing dictionary-formatted observations. E.g., one key:value pair in
        one of these dictionaries could look like:
        '2:37:0:0:0': {'attributes': [0, 2, 0, None],
                       'observations': {'0': [0.331, None],
                                        '10': [0.313, None],
                                        '3': [0.324, None],
                                        '4': [0.307, None],
                                        '5': [0.327, None],
                                        '6': [0.303, None],
                                        '7': [0.32, None],
                                        '8': [0.328, None],
                                        '9': [0.305, None]}}
        Which means we need to use stats_oecd_idd.structure.dimensions.series to "decode" the key, '2:37:0:0:0',
        stats_oecd_idd.structure.attributes.series to decode the 'attributes' key, "[0, 2, 0, None]", and
        stats_oecd_idd.structure.dimensions.observation to line up the keys of "observations" with actual time-periods.

        The important thing to realize here is that even though the JSON pay-load is interpreted as a python dictionary,
        the order the keys is crucial. Hence, the first key in stats_oecd_idd.structure.dimensions.observation[0].values
        will correspond to the '0' key in an observations dictionary.
        """
    metadata_stats_oecd_idd = stats_oecd_idd['structure']['dimensions']

    col_names = []
    for dim in metadata_stats_oecd_idd['series']:
        col_names.append(dim['id'].lower())

    idd_dataframe = pd.DataFrame()

    """
    The observation attributes come in a particularly ordered array, e.g.: [1, 20, 3, None]...
    0  => attributes_stats_oecd_idd['series'][0][1],
    20 => attributes_stats_oecd_idd['series'][1][20],
    3 => attributes_stats_oecd_idd['series'][2][3],
    None => !!! this shouldn't be mapped.
    """

    # need to pull observation statii, if they exist
    observation_status_map = stats_oecd_idd['structure']['attributes']['observation'] # this is incorrectly named and should talk about series
    attribute_series = stats_oecd_idd['structure']['attributes']['series'] # this is incorrectly named and should talk about series
    attribute_column_names = [attribute_map['id'].lower() for attribute_map in attribute_series]
    # = [(x + "_id").lower() for x in attribute_ids]
    # print(attribute_ids)

    # create dummy cases to speed testing
    # pick up ['0:0:1', '0:17:6', '0:1:10']

    test_data = {}
    for x in ['0:0:1', '0:17:6', '0:1:10']:
        test_data[x] = stats_oecd_idd['dataSets'][0]['series'][x]

    observations_dict = test_data # stats_oecd_idd['dataSets'][0]['series']
    for key, value in observations_dict.items():
        """
        Example (key, value):
        ('19:8:0:0:0',
        {'attributes': [0, 20, 0, None],
         'observations': {'0': [43696.0, None], '6': [45934.0, None]}})
        So, extract info from key, and value.attributes
        """
        data = pd.DataFrame(dict(zip(col_names, [[x] for x in key.split(":")])))
        data_attributes = [str(x) for x in
                           value['attributes']]  # metadata should be in string form, since it's categorical
        data = pd.concat([data,
                          pd.DataFrame(dict(zip(attribute_column_names, data_attributes)), index=[0])],
                         axis=1)

        # this needs to be modified to include observation statii
        observations = copy.copy(value['observations'])

        for time, measure in observations.items():
            observations[time] = measure[0]

        observations = pd.DataFrame(list(observations.items()), columns=['time_period', 'observation'])

        observations['location'] = data['location'].iloc[0]

        data = pd.merge(right=data,
                        left=observations,
                        on='location',
                        how='outer')

        idd_dataframe = idd_dataframe.append(data, ignore_index=False)
    return idd_dataframe, metadata_stats_oecd_idd, attribute_series


def append_metadata_to_oecd_stats(idd_dataframe, metadata_stats_oecd_idd, observation_attribute_map):
    """
    Append meta data to OECD stats dataframe:

    the returned JSON has a 'structure' object with 'dimensions'
    child that contains all the information to translate series
    identifiers x:y:z:w:a into something human parse-able.

    A series of merges should be anticipated. Hence, it makes
    sense to store all the metadata in a dictionary where the
    keys will be the merge indices.
    """
    oecd_metadata = {}
    for metadata in [metadata_stats_oecd_idd['series'], observation_attribute_map]:
        for dim in metadata:
            dim_dataframe = pd.DataFrame(dim['values'])
            dim_id = dim['id'].lower()

            # if dim_dataframe is empty, we cannot rename the columns
            try:
                dim_dataframe.columns = [dim_id + '_code', dim_id + '_name']
            except ValueError:
                pass

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
        # no point merging on empty data
        if df.empty:
            continue
        idd_dataframe = pd.merge(left=idd_dataframe,
                                 right=df,
                                 how='left',
                                 on=key)
    return idd_dataframe


def fetch_and_format_oecd_data(idd_base_url='http://stats.oecd.org/sdmx-json/data/IDD',
                               dimension_filter='all',  # grab all data
                               time_filter='all?startTime=2001&endTime=2014',
                               optional_filters='&detail=Full'):
    return append_metadata_to_oecd_stats(
        *fetch_oecd_data(idd_base_url, dimension_filter, time_filter, optional_filters))


if __name__ == "__main__":
    X = append_metadata_to_oecd_stats(*fetch_and_reshape_oecd_json("PDB_GR", "all", "all?detail=Full"))
    X