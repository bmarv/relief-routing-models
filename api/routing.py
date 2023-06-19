from dotenv import dotenv_values
import requests
import openrouteservice as ors


# routing using the openrouteservice api directly
def create_base_configurations_for_ors(
    profile: str = 'driving-car',
    api_key = None
) -> dict: 
    '''
    getting base configuration for api access
    `profile` supports driving_car, foot-walking, bikes
    the `api_key` needs to be located in 'project_directory/.env' or overloaded
    in the parameter `api_key`
    returns a dictionary of configuration items
    '''
    if api_key is None:
        env_vals = dotenv_values(".env")
        ors_api_key = env_vals['ORS_API_KEY']

    config_dict = {
        'base_path': 'https://api.openrouteservice.org/',
        'profile': profile,
        'api_key': ors_api_key,
        'directions_endpoint': 'v2/directions/',
        'geocode_search_endpoint': 'geocode/search'
    }
    return config_dict

def get_from_request(
    params_dict: dict, 
    endpoint_mode = 'directions',
    json_ize = True
) -> dict: 
    '''
    using python requests for get-commands of the direct openrouteservice api
    `params_dict` must reflect the content type of the respective (directions/ geocode-) method
    usable `endpoint_mode` possibilities are `directions` or `geocode`
    '''
    config_dict = create_base_configurations_for_ors()
    params_string = ''
    for k, v in params_dict.items():
        params_string += f'&{k}={v}'
    if endpoint_mode == 'directions':
        request_url = f'{config_dict["base_path"]}{config_dict["directions_endpoint"]}{config_dict["profile"]}?api_key={config_dict["api_key"]}{params_string}'
    elif endpoint_mode == 'geocode':
        request_url = f'{config_dict["base_path"]}{config_dict["geocode_search_endpoint"]}?api_key={config_dict["api_key"]}{params_string}'
    else:
        print('mode not supported')

    r = requests.get(request_url)
    if json_ize:
        return r.json()
    return r

def get_directions_request(
    start_coords: list, 
    end_coords: list
) -> dict: 
    '''
    fires a request for the direct openrouteservice api using the 
    `start_coords` and `end_coords` params, which both accept only 
    a list of pairs of longitudes and latitudes as floating point numbers
    in this exact order
    '''
    start_coords_str = str(start_coords[0]) + ',' + str(start_coords[1])
    end_coords_str = str(end_coords[0]) + ',' + str(end_coords[1])
    params_dict = {
        'start': start_coords_str,
        'end': end_coords_str
    }
    r = get_from_request(
        params_dict= params_dict,
        endpoint_mode= 'directions',
        json_ize= True
    )
    return r

def get_geocode_request(query:str) -> dict: 
    '''
    requests a geocode for a given query and returns a 
    python dictionary with the reponse
    '''
    params_dict = {
        'text': query
    }
    r = get_from_request(
        params_dict= params_dict,
        endpoint_mode= 'geocode',
        json_ize= True
    )
    return r

# routing using openrouteservice-py as one level of indirection
def get_client_ors() -> ors.Client:
    env_vals = dotenv_values(".env")
    ors_api_key = env_vals['ORS_API_KEY']
    client = ors.Client(
        key= ors_api_key
    )
    return client

def get_directions_ors_py(
    start_coords: list, 
    end_coords: list,
    profile: str = 'driving-car',
    client: ors.Client = None,
) -> dict: 
    '''
    calculates route using the module openrouteservice-py as a level of indirection;
    requires the parameters `start_coords` and `end_coords` as a list of floats of 
    each pairs of longitudes and latitudes, if client is not overloaded, a new client 
    element gets instanciated
    '''
    if client is None:
        client = get_client_ors()
    route = client.directions(
        coordinates = [start_coords, end_coords],
        profile = profile,
        format = 'geojson',
        validate = False
    )
    return route

def get_matrix_ors_py(
    coordinates_list: list,
    metrics: list = ['distance', 'duration'],
    profile: str = 'driving-car',
    client: ors.Client = None
) -> dict: 
    '''
    calculates the distance matrix between given points enumerated in `coordinates_list`,
    each listed as a list of floats of logitudes and latitudes. if client is not overloaded, 
    a new client element gets instanciated.
    The returned `matrix` dictionary includes the `metrics` 'distance' or 'duration', if specified
    as a parameter
    '''
    if client is None:
        client = get_client_ors()
    matrix = client.distance_matrix(
        locations=coordinates_list,
        profile=profile,
        metrics=metrics,
        validate=False,
    )
    return matrix