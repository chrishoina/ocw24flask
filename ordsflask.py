from flask import Flask, redirect, render_template, url_for, request, Response
import requests
import jinja2
# import endpoints

app = Flask(__name__)

@app.route('/')
def index():
    import requests

    r1 = requests.get('[BASE PATH]/ords/admin/mymovies/movie-genre')

    genrelist = []

    for i in r1.json()["items"]:
        genre = i['genre']
        genrelist.append(genre)
    # print(genrelist)

    return render_template('index.html', genrelist=genrelist)

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        genre = request.form.get('genre')
        runtime = request.form.get('runtime')
        data1 = {'genre': genre,'runtime': runtime}

        r2 = requests.get('[BASE PATH]/ords/admin/mymovies/movie-all', params=data1)

        data2 = r2.json()
        
        thead = []
        trow = []
        link_keys = []
        link_values = []

        for item in data2['items'][0]:
            thead.append(item)

        for item in data2['items']:
            movie_id = item['movie_id']
            title = item['title']
            genres = item['genres']
            year = item['year']
            abbreviated_summary = item['abbreviated_summary']

            trow.append(item)

        for rel in data2["links"]:
            link_keys.append(rel['rel'])
            link_values.append(rel['href'])
            new_links = zip(link_keys,link_values)
            page_links = dict(new_links)

    return render_template('movieresults.html', thead=thead, trow=trow, page_links=page_links)

@app.route('/next_page', methods=['GET', 'POST'])
def next_page():
    if request.method == 'POST':
        url = request.form.get('next')
        res = requests.get(url)
        # print(response.text)
        newres = res.json()

        thead = []
        trow = []
        link_keys = []
        link_values = []

        for item in newres['items'][0]:
            thead.append(item)
        # print(thead)

        for item in newres['items']:
            movie_id = item['movie_id']
            title = item['title']
            genres = item['genres']
            year = item['year']
            abbreviated_summary = item['abbreviated_summary']
            trow.append(item)
        # print(trow)
        # print(item[0])

        for rel in newres["links"]:
            link_keys.append(rel['rel'])
            link_values.append(rel['href'])
            new_links = zip(link_keys,link_values)
            page_links = dict(new_links)
        # print(page_links)

    return render_template('movieresults.html', thead=thead, trow=trow, page_links=page_links)

@app.route('/previous_page', methods=['GET', 'POST'])
def previous_page():
    if request.method == 'POST':
        url = request.form.get('prev')
        res = requests.get(url)
        # print(response.text)
        newres = res.json()

        thead = []
        trow = []
        link_keys = []
        link_values = []

        for item in newres['items'][0]:
            thead.append(item)
        # print(thead)

        for item in newres['items']:
            movie_id = item['movie_id']
            title = item['title']
            genres = item['genres']
            year = item['year']
            # cast = item['cast']
            abbreviated_summary = item['abbreviated_summary']
            trow.append(item)
        # print(trow)
        # print(item[0])

        for rel in newres["links"]:
            link_keys.append(rel['rel'])
            link_values.append(rel['href'])
            new_links = zip(link_keys,link_values)
            page_links = dict(new_links)
        # print(page_links)

    return render_template('movieresults.html', thead=thead, trow=trow, page_links=page_links)
     
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
