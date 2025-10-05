from flask import Flask, render_template, redirect, request, Response, current_app, make_response, jsonify
import psycopg2
import logging 
import os 
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


app = Flask(__name__)

pool = None

def setup():
    global pool
    load_dotenv()
    print(f"Database URL: {os.environ['DATABASE_URL']}")
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"Creating DB connection Pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        if pool == None: 
            setup()
        connection = pool.getconn()
        yield connection
    finally: 
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def insert_survey_response_into_db(app_name, time_spent_doing_task, time_spent_daily, more_info = None):
    with get_db_cursor(True) as cur: 
        current_app.logger.debug(f"Adding {app_name}, {time_spent_doing_task}, {time_spent_daily}, {more_info}")
        cur.execute(f"INSERT INTO HW1.SURVEY_DB (app, most_time_spent, time_spent, feedback) values (%s, %s, %s, %s)", (app_name, time_spent_doing_task, time_spent_daily, more_info))
    

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/decline')
def decline_page():
    return render_template("decline.html")

@app.route('/survey')
def survey_page():
    return render_template("survey.html")

@app.route('/thanks')
def thanks_page():
    return render_template("thanks.html")

@app.route("/processResponse", methods=["POST"])
def process_response(): 
    if request.method == "POST":
        app_name = request.form['favoriteApp']
        time_spent_doing_task = request.form['phoneActivity']
        time_spent_daily = request.form['timeSpent']
        more_info = request.form['moreInfo'] if request.form['moreInfo'] != "" else None
        insert_survey_response_into_db(app_name, time_spent_doing_task, time_spent_daily, more_info)
        return redirect("/thanks")
    else:
        return
    
def get_survey_results(reverse=False):
    with get_db_cursor(True) as cur: 
        if (not reverse):   
            cur.execute("SELECT * FROM HW1.SURVEY_DB;")
        else:
            cur.execute("SELECT * FROM HW1.SURVEY_DB ORDER BY submitted_at DESC;")
        rows = cur.fetchall()
        return rows
    
def get_time_spent_on_activity_counts(): 
    with get_db_cursor(True) as cur: 
        cur.execute("SELECT DISTINCT most_time_spent, COUNT(*) FROM HW1.SURVEY_DB GROUP BY most_time_spent;")
        return cur.fetchall()
    
def get_daily_time_spent(): 
    with get_db_cursor(True) as cur:
        cur.execute("SELECT DISTINCT time_spent, COUNT(*) FROM HW1.SURVEY_DB GROUP BY time_spent;")
        return cur.fetchall()
    
def get_text_survey_responses():
    with get_db_cursor(True) as cur: 
        cur.execute("SELECT id, app, feedback from HW1.SURVEY_DB order by id;")
        return cur.fetchall()
    
def get_survey_counts_per_day():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT submitted_at::date::text as day, COUNT(*) FROM HW1.SURVEY_DB GROUP BY submitted_at::date ORDER BY submitted_at::date;")
        return cur.fetchall()
    

def get_feedback():
    with get_db_cursor(True) as cur:
        cur.execute("SELECT id, feedback FROM HW1.SURVEY_DB order by id")
        return cur.fetchall()

    
@app.route("/api/results")
def get_api_results():
    reverse = request.args.get('reverse')
    results = get_survey_results(reverse)
    json_results = []
    for row in results:
        json_results.append(dict(row))
    return jsonify(json_results)

@app.route("/admin/summary")
def summary():
    response = {}
    survey_text_responses = get_text_survey_responses()
    # print(f"survey text results: {survey_text_results}")
    survey_text_results = []
    survey_text_dict = {}
    for survey_text_response in survey_text_responses:
        survey_text_dict["id"] = survey_text_response[0]
        survey_text_dict["app"] = survey_text_response[1]
        survey_text_response["feedback"] = survey_text_response[2] if survey_text_response["feedback"] is not None else ""
        survey_text_results.append(survey_text_response)
    response['survey_text_results'] = survey_text_results
    print(f"Survey text results: {survey_text_results}\n")
    activity_counts = dict(get_time_spent_on_activity_counts())
    response['activity_counts'] = activity_counts
    print(f"Activity counts: {response['activity_counts']}")
    time_spent = dict(get_daily_time_spent())
    response['daily_time_spent'] = time_spent
    survey_counts = dict(get_survey_counts_per_day())
    response["survey_counts"] = survey_counts
    print(f"response survey counts: {response['survey_counts']}")
    response['feedback'] = dict(get_feedback())
    return render_template("stats.html", text_results = response['survey_text_results'], activity_results = response['activity_counts'], daily_time_spent = response['daily_time_spent'], survey_count_data = response['survey_counts'])
    



# if __name__ == "__main__":
#     app.run(port=5000, debug=True)