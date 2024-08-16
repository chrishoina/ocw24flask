# The Flask request and requests library are different, hence why both are needed.
# You can see their different usages throughout this script.

from flask import Flask, redirect, render_template, url_for, request, Response
import requests

app = Flask(__name__)

# I reference this as the index page or sometimes the landing page. There are three portions here:
#
#        1. The route, @app.route('/)
#        2. The index function, def index():
#        3. The result of the function is to render an HTML template named 'index.html.'
#
# What you see on the index page is the product of all these "things" combined. The same principles 
# apply to the "movieresults.html" page as well.

@app.route('/')
def index():

    r1 = requests.get("[Your /ords/mymovies/movie-genre endpoint goes here]")

# Here you are creating an empty list, which will be populated with the items from this ORDS API. If you are viewing the
# Handler code, in the Database Actions REST Workshop, then you'll see how a "Unique" list of movie genres
# is being returned in the JSON payload. The nice thing about this approach is that the values in your table can
# change, with little impact on the "front end" because Jinja2 templating is used. The list of movie genres
# can grow, and there isn't anything hard-coded.

    genrelist = []

    for i in r1.json()["items"]:
        genre = i['genre']
        genrelist.append(genre)
    # print(genrelist)

# This portion tells the function to render the index.html file, and pass the genreslist to the template. If you 
# review the "index.html" page, you'll see a reference to the genrelist. Some manipulation is done when the page loads, 
# and that is how Flask is able to render everything all at once.

    return render_template('index.html', genrelist=genrelist)

# I've discussed this route on the "movieresults.html" page. But it's important to understand that this entire 
# application has, for lack of a better term, internal requests, and external requests. An "internal" request is 
# something you see in this route and its function. A user makes two selections on the index/landing page: genre and runtime.
# When they click the "Show me" button, which actually has a type="Submit". Flask recognizes that, BUT it sees that 
# there is a <form> as well. Flask takes the user selections - genre and movie time - that are contained in that entire
# <form> and passes it to this function below. This is what I interpret as an "internal" request. Flask sends this information
# as a POST request, to the handle_data(): function. From there, those selections are packaged up as params (parameters), for 
# an "external" request. That request submits a GET request to the ORDS /movie-all endpoint. 
# 
# If you review the handler code of this endpoint in the Database Actions REST Workshop you will see how these two parameters
# are accepted as input parameters for the SQL handler code. There you'll see how the SQL takes in movie genre and returns results where
# that specific movie genre exists. It's coded in such a way as to allow other genres in the results as well. That is because a row
# in the "genres" table column might have multiple genres. This code asks, "Does the list have genres?" If yes, then a list for that row is
# returned. It also takes in a single parameter for runtime. Here is a great example of where your limitations in SQL or PLSQL might force 
# you to make some...interesting design choices. If you review the handler code, it uses an "equal to or less than" kind of logic. 
# That is a pretty "hungry" request. A better approach might be to allow the user to choose a minimum and maximum runtime. But you have
# to ask yourself the following questions:
# 
#       1. Can you make this "work" with HTML, JavaScript, and CSS, using what you know TODAY?
#       2. Can you create the necessary SQL or PLSQL handler code to even accept this? 
# 
# That might not always be the case. So what you see here is a "concession in code". It gets the job done, but of course there is ALWAYS
# a more clever or elegant way to achieve the end result. 

@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        genre = request.form.get('genre')
        runtime = request.form.get('runtime')
        data1 = {'genre': genre,'runtime': runtime}

        r2 = requests.get("[Your ords/mymovies/movie-all endpoint goes here]", params=data1)

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

# The below code has been referenced throughout. But you'll notice how the "links" of the incoming 
# JSON payload (the payload from the "external" ORDS request) is used to populate the page_links dictionary. That dictionary
# along with the thead and trow variables are passed to the "movieresults.html" page. And, as you'll see in the comments on that
# page, these variables are used for variables in Jinja2 template functions.

        for rel in data2["links"]:
            link_keys.append(rel['rel'])
            link_values.append(rel['href'])
            new_links = zip(link_keys,link_values)
            page_links = dict(new_links)

    return render_template('movieresults.html', thead=thead, trow=trow, page_links=page_links)

# Luckily, the /next_page and /previous_page routes are nearly identical. They are nearly identical to the /handle_data app route too.
# The same "internal" request principle applies to both this and the /previous_page app routes. In this case, you'll see the 
# url = request.form.get('next') portion of code. What is being passed is the actual URI string for the "next" link. I'll explain,
# in another way. If you were to visit directly, IN YOUR BROWSER, the /movie-all endpoint with "params", it might look something
# like this: 
# 
#       "https://[Your server name]/MOVIE/mymovies/movie-all?genre=Comedy&runtime=210" 
# 
# The above is essentially what a user might select on the homepage (i.e., you're just entering this into the browser manually). 
# If you were to take a look at the JSON payload that is returned, you'd notice several "properties": items, hasMore, limit, offset, count, and links.
# And within the links property might exist either a "next" or "previous" link. These links would direct you to the next OR previous
# sets of results. Since we set pagination to 25 results, everything is "stepped" in increments of 25. 
# IF you are on page one of the results, so the first page, AND assuming more results are accessible, then a NEXT link would be made
# available. That next link would look like this:
# 
#       "https://[Your server name]/MOVIE/mymovies/movie-all?genre=Comedy&runtime=210&offset=25"
# 
# That "next", is then used for the below function, and THAT link might also have "next" and "previous" links (all stepped +/- in increments of 25),
# so when applicable, it passes those variables to the "movieresults.html" page and the cycle sort of starts all over again. 
# 
# Again, another example of where trade-offs exist when it comes to coding experience and front-end design experience. Is there 
# a better way? Of course. But the take-home message here is that these ORDS APIs have a lot for you that is already built in. You 
# don't have to worry about coding any counters for page numbers, it's all already there for you. 

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

# There isn't much to expand on here. You've seen this twice by now. Once in the original version found in the 
# /handle_data app route and another time in the /next_page app route. The same thing is accomplished. a URL is passed, 
# and the cycle starts all over again.

# You should know, that the associated "Previous" button, found on the "movieresults.html" page, will initially be disabled ("greyed out").
# And that is because, when a user first makes their selections, and then they are subsequently taken to the "moviesresults.html"
# page, that will, in fact, be the first in a series of results sets (i.e., JSON that is received from an ORDS endpoint). And because
# nothing came before it, a "Previous" link will not be found in the JSON payload. 

# The same eventually will happen with the "Next" button too, but in reverse. Eventually, you will hit the end of the results, and 
# no "Next" link will be included in the ORDS JSON payload. Because there isn't anything left! So you'll have no choice but to click
# the previous button!

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
