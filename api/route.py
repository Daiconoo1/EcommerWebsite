from flask import render_template
from store import app
from flask_googlemaps import GoogleMaps 
from flask_googlemaps import Map

 
GoogleMaps(app, key="AIzaSyCpCay0KlvrI6sKMXzK5-9DPcmrUfh3MNY")

@app.route('/apii')
def viewmap():
	mymap = Map(
        identifier="mymap",
        lat=53.2763709,
        lng=-6.2921546,
        style = "height:400px;width:1130px;margin:3em 0 12em 0;",         
        markers= [
        {
        	 
        	'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        	'lat':53.2763709, 
        	'lng':-6.2921546,
        	'infobox': "<span style='text-align:center'><h3><b>Dublin</b></h3><p><h4>Phone: +353899838294</h4><p><h4>Add: 13 WhiteChurch Lawn</h4></span>"
        	
        }
        ]
              
    )
	 
	return render_template ('api/contact.html', mymap=mymap)

 
