#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = [] # list to store all events
    event_query = Event.query.all() # query all events
    for event in event_query:
        event_dict = body = {
                        "id": event.id,
                        "name": event.name,
                        "location": event.location
                    }
        events.append(event_dict)
    return jsonify(events), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    sessions = [] # list to store all sessions
    event_query = Event.query.filter_by(id=id).first() # get the event_query

    # Make sure the event exists based on id
    if event_query:
        # Loop through the event sessions and add them to the sessions list
        for session in event_query.sessions:
            session_dict = {
                "id": session.id,
                "title": session.title,
                "start_time": session.start_time.isoformat(),
            }
            sessions.append(session_dict)
        return jsonify(sessions), 200
    else:
        error_message = {"error": "Event not found"}
        return jsonify(error_message), 404


@app.route('/speakers')
def get_speakers():
    speakers = [] # list to store all speakers
    speaker_query = Speaker.query.all() # query all speakers
    # Loop through the speakers and add it to a dictionary
    for speaker in speaker_query:
        speaker_dict = body = {
                        "id": speaker.id,
                        "name": speaker.name,
                    }
        speakers.append(speaker_dict)
    return jsonify(speakers), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    # Get the first speaker matching the id
    speaker = Speaker.query.filter_by(id=id).first()

    # Check if the speaker exists then add the speaker information to a dicitonary
    if speaker:
        speaker_dict = {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
        }
        return jsonify(speaker_dict), 200
    else:
        error_message = {"error": "Speaker not found"}
        return jsonify(error_message), 404



@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    speakers = []
    session_query = Session.query.filter_by(id=id).first() 

    if session_query:
        for speaker in session_query.speakers:
            speaker_dict = {
                "id": speaker.id,
                "name": speaker.name,
                "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
            }
            speakers.append(speaker_dict)
        return jsonify(speakers), 200
    else:
        error_message = {"error": "Session not found"}
        return jsonify(error_message), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)