#!./flampparser-env/bin/python3

import requests

# конфиги
IS_TEST = False
PARSE_PLACES = True

# опции
metarubrics = ['bary', 'eda']
citys = ['ekaterinburg', 'moscow']

# урлы
url_places = 'https://flamp.ru/api/2.0/filials/?project={city}&limit={limit}&metarubric={metarubric}&nocache=true' \
             '&page={page}&sort=rating&fields=id,work_hours,nearest_stations,additional_data,reviews_count,' \
             'rating_decimal,lat,lon,photos,name_primary,name_extension,name_description,address,city,adm_div,' \
             'project_id,basic_attributes'
url_reviews = 'https://flamp.ru/api/2.0/filials/{place_id}/reviews?limit=50&is_trusted=true{offset}'


# хидеры
headers = {
    'X-Application': 'Flamp4',
    'Origin': 'https://ekaterinburg.flamp.ru',
    'Authorization': 'Bearer 2b93f266f6a4df2bb7a196bb76dca60181ea3b37',
    'Accept': ';q=1;depth=0;scopes={};application/json',
    'Referer': 'https://ekaterinburg.flamp.ru/',
    'Accept-Encoding': 'gzip, deflate, br'
}


def get_places(metarubric, city, is_test=False):
    places = []
    total = True
    page = 1

    while total is not 0:
        print('Parse page "%s", city "%s", rubric "%s"' % (page, city, metarubric))

        request = requests.get(url_places.format(city=city, limit=50, page=page, metarubric=metarubric), headers=headers)
        places.extend([{
            'id': place['id'],
            'name_primary': place['name_primary'],
            'name_extension': place['name_extension'],
            'city': place['city'],
            'address': place['address'],
            'rating_decimal': place['rating_decimal'],
            'reviews_count': place['reviews_count'],
            'business_lunch': place['basic_attributes']['business_lunch'],
            'avg_price': place['basic_attributes']['avg_price'],
            'reviews': []

        } for place in request.json()['filials']])

        total = request.json()['meta']['total']
        page += 1

        if is_test:
            break

    return places


def get_reviews(place, is_test=False):
    reviews = []
    total = True
    offset = ''

    while total is not 0:
        print('Parse place "%s-%s", offset "%s"' % (place['name_primary'], place['id'], offset))

        request = requests.get(
            url_reviews.format(limit=50, place_id=place['id'], offset=offset),
            headers=headers).json()

        reviews.extend([{
            'id': review['id'],
            'text': review['text'],
            'user': review['user'],
            'rating': review['rating'],
            'likes_score': review['likes_score'],
            'date_created': review['date_created'],
            'official_answer': [{
                'text': answer['text'],
                'date_created': answer['date_created'],
            } for answer in review['official_answer']] if review['official_answer'] else ''
        } for review in request['reviews']])

        offset = '&offset_id=%s' % reviews[-1]['id'] if len(reviews) > 0 else ''
        total = len(request['reviews'])

        if is_test:
            break

    return reviews


# достаем заведения
if PARSE_PLACES:
    places = []

    # собираем заведения
    for metarubric in metarubrics:
        for city in citys:
            places += get_places(metarubric=metarubric, city=city, is_test=IS_TEST)

    # записываем в файл
    with open('dataset_places.json', 'w') as dataset_places:
        dataset_places.write(str(places))
else:
    # читаем заведения из файла
    with open('dataset_places.json', 'r') as dataset_places:
        places = eval(dataset_places.read())

# парсим отзывы
reviews_count = 0
for i, place in enumerate(places):
    places[i]['reviews'] = get_reviews(place, is_test=IS_TEST)
    reviews_count += len(places[i]['reviews'])

# немного статистики
print('Places: %s' % len(places))
print('Reviews: %s' % reviews_count)

# кажется, нам все удалось
with open('dataset_all.json', 'w') as dataset:
    dataset.write(str(places))