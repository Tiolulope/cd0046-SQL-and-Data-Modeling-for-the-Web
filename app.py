from config import *
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format = "EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format = "EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    venues = Venue.query.all()
    locations = set()

    for venue in venues:
        locations.add((venue.city, venue.state))

    for location in locations:
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })

    for venue in venues:
        shows = Show.query.filter_by(venue_id=venue.id).all()
        current_date = datetime.now()

        num_upcoming_shows = 0
        for show in shows:
            if show.start_time > current_date:
                num_upcoming_shows += 1

        for value in data:
            if venue.state == value['state'] and venue.city == value['city']:
                value['venues'].append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming_shows
                })
    return render_template('pages/venues.html', areas=data)
#   data = [{
#       "city": "San Francisco",
#       "state": "CA",
#       "venues": [{
#           "id": 1,
#           "name": "The Musical Hop",
#           "num_upcoming_shows": 0,
#       }, {
#           "id": 3,
#           "name": "Park Square Live Music & Coffee",
#           "num_upcoming_shows": 1,
#       }]
#   }, {
#       "city": "New York",
#       "state": "NY",
#       "venues": [{
#           "id": 2,
#           "name": "The Dueling Pianos Bar",
#           "num_upcoming_shows": 0,
#       }]
#   }]


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

    response = {
        "count": result.count(),
        "data": result
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.get(venue_id)

    upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()
    print(upcoming_shows_query)
    upcoming_shows = []

    past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": format_datetime(str(show.start_time))
        })

    data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

    return render_template('pages/show_venue.html', venue=data)
#   data1 = {
#       "id": 1,
#       "name": "The Musical Hop",
#       "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#       "address": "1015 Folsom Street",
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "123-123-1234",
#       "website": "https://www.themusicalhop.com",
#       "facebook_link": "https://www.facebook.com/TheMusicalHop",
#       "seeking_talent": True,
#       "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#       "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#       "past_shows": [{
#           "artist_id": 4,
#           "artist_name": "Guns N Petals",
#           "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#           "start_time": "2019-05-21T21:30:00.000Z"
#       }],
#       "upcoming_shows": [],
#       "past_shows_count": 1,
#       "upcoming_shows_count": 0,
#   }
#   data2 = {
#       "id": 2,
#       "name": "The Dueling Pianos Bar",
#       "genres": ["Classical", "R&B", "Hip-Hop"],
#       "address": "335 Delancey Street",
#       "city": "New York",
#       "state": "NY",
#       "phone": "914-003-1132",
#       "website": "https://www.theduelingpianos.com",
#       "facebook_link": "https://www.facebook.com/theduelingpianos",
#       "seeking_talent": False,
#       "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
#       "past_shows": [],
#       "upcoming_shows": [],
#       "past_shows_count": 0,
#       "upcoming_shows_count": 0,
#   }
#   data3 = {
#       "id": 3,
#       "name": "Park Square Live Music & Coffee",
#       "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#       "address": "34 Whiskey Moore Ave",
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "415-000-1234",
#       "website": "https://www.parksquarelivemusicandcoffee.com",
#       "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#       "seeking_talent": False,
#       "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#       "past_shows": [{
#           "artist_id": 5,
#           "artist_name": "Matt Quevedo",
#           "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#           "start_time": "2019-06-15T23:00:00.000Z"
#       }],
#       "upcoming_shows": [{
#           "artist_id": 6,
#           "artist_name": "The Wild Sax Band",
#           "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#           "start_time": "2035-04-01T20:00:00.000Z"
#       }, {
#           "artist_id": 6,
#           "artist_name": "The Wild Sax Band",
#           "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#           "start_time": "2035-04-08T20:00:00.000Z"
#       }, {
#           "artist_id": 6,
#           "artist_name": "The Wild Sax Band",
#           "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#           "start_time": "2035-04-15T20:00:00.000Z"
#       }],
#       "past_shows_count": 1,
#       "upcoming_shows_count": 1,
#   }
#   data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)

    try:
        venue = Venue()
        form.populate_obj(venue)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    finally:
        db.session.close()

    return render_template('pages/home.html')
#   # TODO: insert form data as a new Venue record in the db, instead
#   # TODO: modify data to be the data object returned from db insertion

#   # on successful db insert, flash success
#   flash('Venue ' + request.form['name'] + ' was successfully listed!')
#   # TODO: on unsuccessful db insert, flash an error instead.
#   # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
#   # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#   return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue_name = venue.name

    db.session.delete(venue)
    db.session.commit()

    flash('Venue ' + venue_name + ' was deleted')
  except:
    flash('an error occured and Venue ' + venue_name + ' was not deleted')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []

  for artist in artists:
      data.append({
          "id": artist.id,
          "name": artist.name
      })

  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    search_term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    response = {
        "count": result.count(),
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
#   response = {
#       "count": 1,
#       "data": [{
#           "id": 4,
#           "name": "Guns N Petals",
#           "num_upcoming_shows": 0,
#       }]
#   }
  #return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)

    if not artist:
        return render_template('errors/404.html')

    upcoming_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    print(upcoming_shows_query)
    upcoming_shows = []

    past_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": format_datetime(str(show.start_time))
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": format_datetime(str(show.start_time))
        })

    print(artist.genres)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=data)
#   data1 = {
#       "id": 4,
#       "name": "Guns N Petals",
#       "genres": ["Rock n Roll"],
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "326-123-5000",
#       "website": "https://www.gunsnpetalsband.com",
#       "facebook_link": "https://www.facebook.com/GunsNPetals",
#       "seeking_venue": True,
#       "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#       "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#       "past_shows": [{
#           "venue_id": 1,
#           "venue_name": "The Musical Hop",
#           "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#           "start_time": "2019-05-21T21:30:00.000Z"
#       }],
#       "upcoming_shows": [],
#       "past_shows_count": 1,
#       "upcoming_shows_count": 0,
#   }
#   data2 = {
#       "id": 5,
#       "name": "Matt Quevedo",
#       "genres": ["Jazz"],
#       "city": "New York",
#       "state": "NY",
#       "phone": "300-400-5000",
#       "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#       "seeking_venue": False,
#       "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#       "past_shows": [{
#           "venue_id": 3,
#           "venue_name": "Park Square Live Music & Coffee",
#           "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#           "start_time": "2019-06-15T23:00:00.000Z"
#       }],
#       "upcoming_shows": [],
#       "past_shows_count": 1,
#       "upcoming_shows_count": 0,
#   }
#   data3 = {
#       "id": 6,
#       "name": "The Wild Sax Band",
#       "genres": ["Jazz", "Classical"],
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "432-325-5432",
#       "seeking_venue": False,
#       "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "past_shows": [],
#       "upcoming_shows": [{
#           "venue_id": 3,
#           "venue_name": "Park Square Live Music & Coffee",
#           "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#           "start_time": "2035-04-01T20:00:00.000Z"
#       }, {
#           "venue_id": 3,
#           "venue_name": "Park Square Live Music & Coffee",
#           "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#           "start_time": "2035-04-08T20:00:00.000Z"
#       }, {
#           "venue_id": 3,
#           "venue_name": "Park Square Live Music & Coffee",
#           "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#           "start_time": "2035-04-15T20:00:00.000Z"
#       }],
#       "past_shows_count": 0,
#       "upcoming_shows_count": 3,
#   }
#   data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  #

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm()
  form = ArtistForm(obj=artist)

 # artist = {
#       "id": 4,
#       "name": "Guns N Petals",
#       "genres": ["Rock n Roll"],
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "326-123-5000",
#       "website": "https://www.gunsnpetalsband.com",
#       "facebook_link": "https://www.facebook.com/GunsNPetals",
#       "seeking_venue": True,
#       "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#       "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
#   }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)

    try:
        form.populate_obj(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully edited!')

    except:
        db.session.rollback()
        flash('An error occurred. artist ' +
              request.form['name'] + ' could not be edited.')
    finally:
        db.session.close()

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)
#   venue = {
#       "id": 1,
#       "name": "The Musical Hop",
#       "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#       "address": "1015 Folsom Street",
#       "city": "San Francisco",
#       "state": "CA",
#       "phone": "123-123-1234",
#       "website": "https://www.themusicalhop.com",
#       "facebook_link": "https://www.facebook.com/TheMusicalHop",
#       "seeking_talent": True,
#       "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#       "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
#   }
  # TODO: populate form with values from venue with ID <venue_id>
    #return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

    form = VenueForm(request.form)

    try:
        venue = Venue.query.get(venue_id)
        form.populate_obj(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully edited!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be edited.')

    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  #   # called upon submitting the new artist listing form
  #   # TODO: insert form data as a new Venue record in the db, instead
  #   # TODO: modify data to be the data object returned from db insertion

  #   # on successful db insert, flash success
  #   flash('Artist ' + request.form['name'] + ' was successfully listed!')
  #   # TODO: on unsuccessful db insert, flash an error instead.
  #   # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

    form = ArtistForm(request.form)
    try:
        artists = Artist()
        form.populate_obj(artists)
        print(artists.id)
        print(artists.id)
        db.session.add(artists)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('Failed to create artist ' + request.form['name'])
        print(sys.exc_info)
    finally:
        db.session.close()

    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
   shows = Show.query.all()
   data = []

   for show in shows:
       data.append({
           "venue_id": show.venue_id,
           "venue_name": show.venue.name,
           "artist_id": show.artist_id,
           "artist_name": show.artist.name,
           "artist_image_link": show.artist.image_link,
           "start_time": format_datetime(str(show.start_time))
       })
   return render_template('pages/shows.html', shows=data)
#   data = [{
#       "venue_id": 1,
#       "venue_name": "The Musical Hop",
#       "artist_id": 4,
#       "artist_name": "Guns N Petals",
#       "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#       "start_time": "2019-05-21T21:30:00.000Z"
#   }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "artist_id": 5,
#       "artist_name": "Matt Quevedo",
#       "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#       "start_time": "2019-06-15T23:00:00.000Z"
#   }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-01T20:00:00.000Z"
#   }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-08T20:00:00.000Z"
#   }, {
#       "venue_id": 3,
#       "venue_name": "Park Square Live Music & Coffee",
#       "artist_id": 6,
#       "artist_name": "The Wild Sax Band",
#       "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#       "start_time": "2035-04-15T20:00:00.000Z"
#   }]
#   return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
      form = ShowForm(request.form)
      show = Show()
      form.populate_obj(show)
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      flash('Failed to create show')
  finally:
      db.session.close()
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
