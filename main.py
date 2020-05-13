import time

import redis
import datetime
from io import StringIO
from flask import Flask, render_template, request, redirect, Response
from scrapper import scrape_page

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

db = {}
app = Flask("Jobs")

jobList = set()
pages = [
    "weworkremotely",
    "stackoverflow",
    "remoteok"
]

@app.route("/")
def home():
  return render_template("home.html", pages=pages, jobList = jobList )


@app.route("/add", methods=["post"])
def add():
  newJob = request.form['new-jobname']
  newJob = newJob.capitalize()
  if(newJob in pages):
    print("sites can't search")
  elif(newJob in jobList):
    print("already exists")
  else:
    jobList.add(newJob)
  return render_template("home.html", pages=pages,  jobList = jobList)

@app.route("/read", methods=["post"])
def read():

  global db

  existingPages = {}

  selectedPages = set()
  selectedJobs = set()

  for item in request.form:
    if( item in pages):
      selectedPages.add(item)
    if( item in jobList):
      selectedJobs.add(item)

  if not selectedPages:
    selectedPages = set(pages)

  print(selectedPages)
  print(selectedJobs)

  for page in selectedPages:
    existingPages[page] = db.get(page)
    if not existingPages[page]:
      tempScrapper = {}
      tempScrapper['0'] = scrape_page(page)
      existingPages[page] = tempScrapper
      db[page] = existingPages[page]

  if selectedJobs:
    for job in selectedJobs:
      for page in selectedPages:
        existingPages[page][job] = db[page].get(job)
        if not existingPages[page][job]:
          tempScrapper = {}
          print(page,job)
          tempScrapper = scrape_page(page,job)
          existingPages[page][job] = tempScrapper
          db[page][job] = existingPages[page][job]

  posts = {}

  if selectedJobs:
    for page in selectedPages:
      posts[page] = {}
      for job in selectedJobs:
        posts[page][job] = existingPages[page][job]
  else:
    print("no jobs!! print ALL!")
    for page in selectedPages:
      posts[page] = {}
      posts[page]['0'] = existingPages[page]['0']
  return render_template("read.html", selected=selectedPages, jobs=selectedJobs, posts=posts)

@app.route("/extract", methods=["post"])
def extract():

  global db

  selectedPages = set()
  selectedJobs = set()

  for item in request.form:
    print(item)
    if( item in pages):
      selectedPages.add(item)
    if( item in jobList):
      selectedJobs.add(item)

  if not selectedPages:
    selectedPages = set(pages)

  if not selectedJobs:
    selectedJobs.add('0')

  print(selectedPages)
  print(selectedJobs)

  try:
    print("csv만들어요!")
    csv = StringIO()
    csv.write("site, keyword, company, location, title, link\n")
    print("csv써요!!!")
    for page in selectedPages:#검색장소
      for job in selectedJobs:#검색어
        print(f"검색 DB : {page}{job}")
        for item in db[page][job]:#디비
          csv.write(str(page))
          csv.write(",")
          csv.write(str(job))
          csv.write(",")
          for i, value in enumerate(item):
            csv.write(str(value))
            if(i < len(item)):
              csv.write(",")
          csv.write("\n")
    print("옹")
    date = datetime.datetime.now()
    date = date.strftime('%Y%m%d%H%M%S')
    response = Response(
        csv.getvalue(),
        mimetype='text/csv',
        content_type="application/octet-stream",
    )
    response.headers["Content-Disposition"] =f"attachment; filename=JobFinder_{date}.csv"
    return response
  except Exception:
    return redirect("/")

@app.route("/db")
def database():
  return render_template("db.html", db=db)

app.run(host="0.0.0.0")