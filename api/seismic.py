import requests

def create_base_configurations() -> dict: 
    '''
    getting base configuration for api access to seismic data
    returns a dictionary of configuration items
    '''
    config_dict = {
        'base_path': 'https://earthquake.usgs.gov/fdsnws/event/1/',
        'count_method': 'count?format=geojson',
        'query_method': 'query?format=geojson'
    }
    return config_dict

def get_from_request(
    params_dict: dict, 
    json_ize = True
) -> dict: 
    '''
    using python requests for get-commands of the direct seismic api from usgs.gov
    `params_dict` must reflect the start and endtime format
    returns a json-ized response
    '''
    config_dict = create_base_configurations()
    params_string = ''
    for k, v in params_dict.items():
        params_string += f'&{k}={v}'
    query_url = f'{config_dict["base_path"]}{config_dict["query_method"]}&{params_string}'

    r = requests.get(query_url)
    if json_ize:
        return r.json()
    return r

def get_earthquakes_within_start_and_endtime(
    starttime: str,
    endtime: str
)-> dict:
    '''
    accepts `starttime` and `endtime` parameters of the following format: yyyy-mm-dd
    as a string.
    runs a get-requests for the specified timeframe to find earthquakes
    '''
    params_dict = {
        'starttime': starttime,
        'endtime': endtime
    }
    r = get_from_request(
        params_dict= params_dict,
        json_ize= True
    )
    return r

def post_process_earthquake_results(
    response_dict: dict,
    element: int,
    mode: str
):
    '''
    yields results for magnitudes, coordinates or ids if specified in `mode`
    for a numerical `element` in the `response_dict`.
    '''
    if mode == 'magnitude':
        return response_dict['features'][element]['properties']['mag']
    elif mode == 'coordinates':
        return response_dict['features'][element]['geometry']['coordinates']
    elif mode == 'ids':
        return response_dict['features'][element]['properties']['ids']
    else:
        return {
            'magnitude': response_dict['features'][element]['properties']['mag'],
            'coordinates': response_dict['features'][element]['geometry']['coordinates'],
            'ids': response_dict['features'][element]['properties']['ids']
        }