import googlemaps as gm
import pandas as pd

from infoExtraction import add_to_dic

key = 'AIzaSyAmx0c-Oqr8XPUVYpO63tJ8eLe9AV-8a6w'

client = gm.Client(key=key)

''' Convert file coordinates to string for distance calculation'''


def coordsToString(dic):

    loc = str(dic['latitude']) + ', ' + str(dic['longitude'])

    return loc


'''Given source and desticanition strings, returns the duration"'''


def get_duration(source, dest):

    direction = client.directions(source, dest, mode='walking')

    duration = direction[0]['legs'][0]['duration']['text']
    duration = int(duration.split(' ')[0])

    return duration


''' Filter dataset to places within 7 min walking distance from a museum's coordinates '''


def filter_walking_distance(df, museum):
    walking_distance = []

    for i, coord in enumerate(df['coordinate']):
        
        dest = coordsToString(coord)
        
        if get_duration(museum, dest) < 6:
            walking_distance.append(i)

    filtered = df.iloc[walking_distance].dropna(axis=1, how='all')
    
    return filtered


''' Extract relevant information per place and return as dictionary '''


def get_details(row):

    dic = {}
    for label, value in row.dropna().items():

        if label == 'coordinate':
            result = client.reverse_geocode(coordsToString(value))
            address = result[0]['formatted_address']

            dic['Address'] = address.replace(', Belgium', '')
            dic['Coordinates'] = value

        elif label == 'amenity':
            dic = add_to_dic(dic, 'Amenity', value)

        elif label == 'name':
            dic = add_to_dic(dic, 'Name', value)

        elif label == 'opening_hours':
            dic = add_to_dic(dic, 'Opening hours', value)

        elif 'phone' in label:
            dic = add_to_dic(dic, 'Phone number', value)

        elif 'website' in label:
            dic = add_to_dic(dic, 'Website', value)

        elif 'email' in label:
            dic = add_to_dic(dic, 'Email', value)

        elif label == 'cuisine':
            dic = add_to_dic(dic, 'Cuisine', value)

        elif label == 'brand':
            dic = add_to_dic(dic, 'Brand', value)

        elif label == 'outdoor_seating':
            dic = add_to_dic(dic, 'Outdour seating', value)

        elif label == 'internet_access':
            dic = add_to_dic(dic, 'Wifi', value)

        elif label == 'brewery':
            dic = add_to_dic(dic, 'Brewery', value)

        elif label == 'theme':
            dic = add_to_dic(dic, 'Theme', value)

        elif 'diet' in label:
            dic = add_to_dic(dic, 'Diet', value)

        elif 'payment' in label:
            dic = add_to_dic(dic, 'Payment', value)

        elif label == 'screen':
            dic = add_to_dic(dic, 'Screen', value)

        elif 'wheelchair' in label:
            dic = add_to_dic(dic, 'Wheelchair', value)

        elif label == 'smoking':
            dic = add_to_dic(dic, 'Smoking', value)

        elif label == 'min_age':
            dic = add_to_dic(dic, 'Minimum age', value)

        elif label == 'lgbtq':
            dic = add_to_dic(dic, 'LGBTQ', value)

        elif label == 'microbrewery':
            dic = add_to_dic(dic, 'Microbrewery', value)

        elif label == 'food':
            dic = add_to_dic(dic, 'Food', value)

        elif label == 'air_conditioning':
            dic = add_to_dic(dic, 'Air conditioning', value)

        elif label == 'delivery':
            dic = add_to_dic(dic, 'Delivery', value)

        elif label == 'cocktails':
            dic = add_to_dic(dic, 'Cocktails', value)

    return dic

''' Recommend places based on museum '''
def recommended_places(museum):
    
    df = pd.read_json('..\..\datasets\POI\pois.json')

    museum_coords = {'alijn': '51.05755362299733, 3.723522739298267', 'design': '51.05590007151709, 3.719668184088063',
                     'industrie': ' 51.059572076526635, 3.729351512923772', 'stam': '51.04408963545599, 3.7175096975808697', 'archief': '51.04584607079588, 3.7505423487840495'}

    amenities = ['restaurant', 'cafe', 'bar', 'cinema', 'nightclub', 'ice_cream', 'theatre']

    df = df[df['amenity'].isin(amenities)]
    df = df.reset_index(drop=True).dropna(axis=1, how='all')

    source = museum_coords[museum]

    df = filter_walking_distance(df, source)

    places = []

    limits = {'restaurant': 2, 'cafe': 1, 'bar': 1, 'pub': 1, 'theatre': 1, 'ice_cream': 1, 'nightclub': 1, 'cinema': 1}

    def update_limit(place):
        limits[place] -= 1
        return limits[place]

    df['details'] = df.apply(get_details, axis=1)
    df['place'] = df['details'].apply(lambda details: details['Amenity'][0])
    df['place_limit'] = df['place'].apply(update_limit)
    
    filtered = df[df['place_limit'] >= 0]
    
    places = filtered['details'].tolist()
            
    return places