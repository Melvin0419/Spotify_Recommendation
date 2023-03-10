from flask import Flask, render_template,request,render_template_string
from note import*

token = get_token()
selections = {"artists":[],"tracks":[],"genres":[]}
artists = []


app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
    # if request.method == "POST":
        
    #     artist = request.form.get('artist')
    #     track = request.form.get('track')

    #     if artist:
    #         artists = search_for_artist(token, artist)
    #         return render_template("home.html", artists = artists)
            
        # if track:
        #     tracks = search_for_track(token, track)

    return render_template("home.html")

@app.route("/<name>",methods=["GET","POST"])
def search(name):
    
    # assign globe var. artists
    global artists
    artists = search_for_artist(token, name)

    # check if artist exist
    if type(artists) == str:
        template = "<h5>{{artists}}</h5>"
    else:
        template = "<ul>{% for artist in artists %}<li> <div class = 'btn artist_select'>{{ artist['name'] }}</div></li>{% endfor %}</ul>"

    # Render the template with the processed data
    html = render_template_string(template, artists=artists)
    return html
    
@app.route("/store_select",methods=["GET","POST"])
def store_select():
    if request.method == "POST":
        selection = request.form["data"]

        global selections
        for artist in artists:
            if artist["name"] == selection:
                selections["artists"].append(artist)

        template1 = "<h5> your selection: {{selection}} </h5>"
        template2 = "<div class='float-right'><li class = 'list-group-item'>{% for selection in selections['artists'] %}<button class='close' type='button'><span aria-hidden='true'> &times;</span></button>{{ selection['name'] }}</li>{% endfor %}</div>"
        html = render_template_string(template1+template2, selection = selection, selections=selections)
    return html


app.run(debug=True)