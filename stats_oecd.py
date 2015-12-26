import json
import urllib.request
import pandas as pd
import numpy as np
import copy


def fetch_and_reshape_oecd_json(data_code,
                                dimension_filter='all',
                                time_and_other_filters='all?detail=Full&dimensionAtObservation=allDimensions'):
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
        + their observation codes are T_GDPPOP_V, T_GDPHRS_
    * and we want to look at these measures through the perspectives of
        + a valued indexed according to observation at 2010
            - this has attribute code 2010Y
        + Annual growth/change,
            - this has attribute code GR
        + Average growth rate
            - this has attribute code AVGRW
    * we want all data between 1970 and 2014
        + we can use the filter "all?startTime=1970&endTime=2014"
    * we want the full detail of the data:
        + append "&detail=Full" to our time_period filter

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
        how the time_period (and detail) dimensions should be filtered. See function description

    :returns: a pandas DataFrame.

    Example input for a request for Income Disparity Data:

    idd_base_url = 'http://stats.oecd.org/sdmx-json/data/IDD'
    dimension_filter = 'all' # grab all data
    time_filter = 'all?startTime=2001&endTime=2014'
    optional_filters = '&detail=Full' # pick up the observation unit's...
    """

    """parse json data into DataFrame:

    the json comes with a 'structure' section which explains how to
    interpret the keys (e.g. 1:2:3:4:5) for the series_observations.

    We first need to parse the 'structure' to figure out what the
    dimension names (and order) is. Then, we need to unpack
    observation values into floats (as opposed to arrays)
    """
    idd_base_url = "http://stats.oecd.org/sdmx-json/data"
    data_query = idd_base_url + '/' + data_code + '/' + dimension_filter + '/' + time_and_other_filters
    oecd_json = json.loads(urllib.request.urlopen(data_query).read().decode('utf-8'))

    """
    oecd_json is a dictionary with keys:
        + structure -- a dict with keys ['annotations', 'attributes', 'dimensions', 'links', 'name', 'description'].
        These keys hold dictionaries as values, whose keys yield further information about the data structure. E.g.:
            - attributes yields a dict with keys ['dataSet', 'observation', 'series']
            - dimensions yields a dict with keys ['observation', 'series']
        Hence, structure.attributes.series contains information about the series' attributes, and
        structure.dimensions.observation yields information about the dimension of series_observations.
        + dataSets -- a list containing dictionary-formatted series_observations. E.g., one dimension_encoding:series
        pair in one of these dictionaries could look like:
        '2:37:0:0:0': {'attributes': [0, 2, 0, None],
                       'series_observations': {'0': [0.331, None],
                                        '10': [0.313, None],
                                        '3': [0.324, None],
                                        '4': [0.307, None],
                                        '5': [0.327, None],
                                        '6': [0.303, None],
                                        '7': [0.32, None],
                                        '8': [0.328, None],
                                        '9': [0.305, None]}}
        Which means we need to use oecd_json.structure.dimensions.series to "decode" the dimension_encoding,
        '2:37:0:0:0', oecd_json.structure.attributes.series to decode the 'attributes' dimension_encoding,
        "[0, 2, 0, None]", and oecd_json.structure.dimensions.observation to line up the keys of "series_observations"
        with actual time_period-periods.

        The important thing to realize here is that even though the JSON pay-load is interpreted as a python dictionary,
        the order the keys is crucial. Hence, the first dimension_encoding in
        oecd_json.structure.dimensions.observation[0].values will correspond to the '0' dimension_encoding in an
        series_observations dictionary.
        """
    oecd_structure = oecd_json['structure']

    """
    When using a flat-format (e.g. appending '&dimensionAtObservation=allDimensions' to the end of the API request),
    the returned payload looks something like:
    oecd_json.dataSets[0] = {
        '0:10:6:9': [0.581259, 0, None, 0, 0, None],
        '0:11:10:10': [61.210162, 0, None, 1, 0, 0],
        '0:1:9:40': [1.40398, 1, None, 0, 0, None]
    }
    Which means the :-separated string in the beginning encodes the time-dimension as the last digit.
    Moreover, we can separate the reshaping task into two parts:
        1. decode the :-separated string using oecd_json.structure.dimensions.observation
        2. properly identify the observation attributes with oecd_json.attributes.observation
    """

    test_data = {}
    for x in ['0:10:6:9', '0:11:10:10', '0:1:9:40']:
        test_data[x] = oecd_json['dataSets'][0]['observations'][x]

    column_names = []
    dimensions_and_attributes = {}

    for dimension in oecd_structure['dimensions']['observation']:
        dimension_name = dimension['id'].lower()
        column_names.append(dimension_name)
        dimensions_and_attributes[dimension_name] = pd.DataFrame(dimension['values'])

    column_names.append('observation')

    for attribute in oecd_structure['attributes']['observation']:
        attribute_name = attribute['id'].lower()
        column_names.append(attribute_name)
        dimensions_and_attributes[attribute_name] = pd.DataFrame(attribute['values'])

    output = []
    for dimensions, observation in test_data.items():
        # make sure dimensions are appropriately cast as integers -- this helps merge along
        # an index later and convert None's to NaN's
        output.append([int(dimension) for dimension in dimensions.split(':')] + \
                      [obs_or_attr if obs_or_attr is not None else np.nan for obs_or_attr in observation])

    output = pd.DataFrame(output, columns=column_names)

    print(output.dtypes)

    for column_name, value_map in dimensions_and_attributes.items():
        value_map.columns = [column_name + '_code', column_name + '_name']
        output = pd.merge(left=output,
                          right=value_map,
                          left_on=column_name,
                          right_index=True,
                          how='left',
                          sort=False)
    print(output)



    # process series

    series_structure = {
        'dimensions': oecd_structure['dimensions']['series'],
        'attributes': oecd_structure['attributes']['series']
    }

    series_data_column_names = []

    series_dimension_names = []
    for series_dimension in series_structure['dimensions']:
        dimension_name = series_dimension['id'].lower()
        series_dimension_names.append(dimension_name)
        series_data_column_names.append(dimension_name)

    series_attribute_names = []
    for attribute in series_structure['attributes']:
        attribute_name = attribute['id'].lower()
        series_attribute_names.append(attribute_name)
        series_data_column_names.append(attribute_name)

    # process observation -- there has to be a better way to do this

    observation_structure = {
        'dimensions': oecd_structure['dimensions']['observation'],
        'attributes': oecd_structure['attributes']['observation']
    }

    observation_data_column_names = ['observation']

    observation_attribute_names = []
    for attribute in observation_structure['attributes']:
        attribute_name = attribute['id'].lower()
        observation_attribute_names.append(attribute_name)
        observation_data_column_names.append(attribute_name)

    observation_dimension_names = []
    for observation_dimension in observation_structure['dimensions']:
        dimension_name = observation_dimension['id'].lower()
        observation_dimension_names.append(dimension_name)
        observation_data_column_names.append(dimension_name)

    """
    The observation attributes come in a particularly ordered array, e.g.: [1, 20, 3, None]...
    0  => attributes_stats_oecd_idd['series'][0][1],
    20 => attributes_stats_oecd_idd['series'][1][20],
    3 => attributes_stats_oecd_idd['series'][2][3],
    None => !!! this shouldn't be mapped.
    """

    # need to pull observation statii, if they exist
    observation_status_map = oecd_json['structure']['attributes']['observation'] # this is incorrectly named and should talk about series
    #attribute_series = series_structure['attributes'] #oecd_json['structure']['attributes']['series'] # this is incorrectly named and should talk about series

    """
    incorporate pattern declared above -- lines 121-127
    """

    # create dummy cases to speed testing
    # pick up ['0:0:1', '0:17:6', '0:1:10']

    test_data = {}
    for x in ['0:0:1', '0:17:6', '0:1:10']:
        test_data[x] = oecd_json['dataSets'][0]['series'][x]

    observations_dict = test_data   # oecd_json['dataSets'][0]['series']

    oecd_dataframe = pd.DataFrame()

    for dimension_encoding, series in observations_dict.items():
        """
        Example (dimension_encoding, series):
        ('19:8:0:0:0',
        {'attributes': [0, 20, 0, None],
         'series_observations': {'0': [43696.0, None], '6': [45934.0, None]}})
        So, extract info from dimension_encoding, and series.attributes
        """

        series_data = [[dimension_value] for dimension_value in dimension_encoding.split(":")]
        for attribute_value in series['attributes']:
            series_data.append([str(attribute_value)])

        data = pd.DataFrame(dict(zip(series_data_column_names, series_data)))

        series_observations = []

        for time_period, observation in series['observations'].items():
            #tmp = {}

            observation_data = [observation[0:1]]
            for obs_status in observation[1:]:
                observation_data.append([obs_status])

            observation_data.append(time_period) # this may have to get changed in the structure of 'observations' changes

            observation_data = dict(zip(observation_data_column_names, observation_data))
            tmp = pd.DataFrame(observation_data)
            series_observations.append(tmp)

        series_observations = pd.concat(series_observations)
        # add on location column for left-merge.
        series_observations['location'] = data['location'].iloc[0]

        data = pd.merge(right=data,
                        left=series_observations,
                        on='location',
                        how='outer')

        oecd_dataframe = oecd_dataframe.append(data, ignore_index=False)

    """
    now we need to merge on metadata. Go back and refactor column situation inside the loop
    """
    print(oecd_dataframe)
    return oecd_dataframe, oecd_json_structure_dimensions, series_structure['attributes']


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
                               optional_filters='&dimensionAtObservation=allDimensions&detail=Full'):
    return append_metadata_to_oecd_stats(
        *fetch_oecd_data(idd_base_url, dimension_filter, time_filter, optional_filters))


if __name__ == "__main__":
    X = append_metadata_to_oecd_stats(*fetch_and_reshape_oecd_json("PDB_GR", "all", "all?detail=Full&dimensionAtObservation=allDimensions"))
    X