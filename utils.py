import ast

# zamiana stringa w liste

def convert(text):
    l = []
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l


def director(text):
    l = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l


def remove_space(word):
    l = []
    for i in word:
        l.append(i.replace(' ', ''))
    return l


def clean_data(data):
    data = data[['movie_id', 'title_x', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    data = data.rename(columns={'title_x': 'title'})
    data['overview'] = data['overview'].fillna('')

    data['genres'] = data['genres'].apply(convert)
    data['keywords'] = data['keywords'].apply(convert)
    data['cast'] = data['cast'].apply(convert)
    data['crew'] = data['crew'].apply(director)
    data.rename(columns={'crew': 'director'}, inplace=True)
    data['overview'] = data['overview'].apply(lambda x: x.split())
    data['cast'] = data['cast'].apply(remove_space)
    data['director'] = data['director'].apply(remove_space)
    data['genres'] = data['genres'].apply(remove_space)
    data['keywords'] = data['keywords'].apply(remove_space)
    return data


def create_tags(data):
    data['tags'] = data['overview'] + data['genres'] + data['keywords'] + data['cast'] + data['director']
    new_df = data[['movie_id', 'title', 'tags']]
    return new_df


def prepare_tags(data):
    data['tags'] = data['tags'].apply(lambda x: " ".join(x))
    data['tags'] = data['tags'].apply(lambda x: x.lower())
    return data
