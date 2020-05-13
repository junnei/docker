import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def scrape_weworkremotely(search=""):
  posts = []

  # searching for all jobs
  # or search by keyword
  if(search==""):
    url = "https://weworkremotely.com"
  else:
    url = f"https://weworkremotely.com/remote-jobs/search?term={search}"
  request = requests.get(url, headers=headers)
  soup = BeautifulSoup(request.text, "html.parser")
  allJobs = soup.find_all("section", {"class":"jobs"})
  for jobList in allJobs:
    jobs = jobList.find_all("li")
    for job in jobs:
      if('view-all' in job['class']):
        continue
      datas = job.find_all("a")
      for i in datas:
        if( "/remote-jobs/" in i['href']):
          data = i
      company = data.find("span",{"class":"company"}).text
      title = data.find("span",{"class":"title"}).text
      try:
        location = data.find("span",{"class":"region"}).text
      except:
        location = None
      link = "https://weworkremotely.com" + data['href']
      posts.append([company, location, title, link])
  print("weworkremotely :",len(posts))
  return posts



def scrape_stackoverflow(search=""):

  posts = []

  # searching for all jobs
  # or search by keyword
  if(search==""):
    url = "https://stackoverflow.com/jobs?r=true"
  else:
    url = f"https://stackoverflow.com/jobs?r=true&q=f{search}"

  request = requests.get(f"{url}", headers=headers)
  soup = BeautifulSoup(request.text, "html.parser")

  # pagination counting - '1 page' doesn't have pagination
  try:
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")[-2].text
  except:
    pages = 1

  # searching each of pages
  for page in range(1,int(pages)+1):
    request_page = requests.get(f"{url}&pg={page}", headers=headers)
    soup_page = BeautifulSoup(request_page.text, "html.parser")
    # 0 jobs : 광고제거
    if(soup_page.find("span",{"class":"description fc-light fs-body1"}).text.strip('') == "0 jobs"):
      break
    allJobs = soup_page.find("div", {"class":"listResults"}).find_all("div",{"class":"grid--cell fl1"})
    for job in allJobs:
      data = job.find("a")

      link = "https://stackoverflow.com" + data['href']
      title = data['title']

      datas = job.find("h3").find_all("span")
      
      company = datas[0].text.strip("\r\n ")
      location = datas[1].text.strip("\r\n ")
      
      posts.append([company, location, title, link])
  print("stackoverflow :",len(posts))
  return posts


def scrape_remoteok(search=""):

  posts = []

  # searching for all jobs
  # or search by keyword
  if(search==""):
    url = "https://remoteok.io"
  else:
    url = f"https://remoteok.io/remote-dev+{search}-jobs"
  request = requests.get(url, headers=headers)
  soup = BeautifulSoup(request.text, "html.parser")
  pages = soup.find("table",{"id":"jobsboard"})
  try:
    job = pages.find_all("tr",{"class":"job"})
    for info in job:
      data = info.find("td",{"class":"company position company_and_position"})
      link =  "https://remoteok.io" + data.find("a",{"itemprop":"url"})['href']
      title = data.find("h2",{"itemprop":"title"}).text
      company = data.find("h3",{"itemprop":"name"}).text
      location = info.find("td",{"class":"location tooltip-set"}).text
      
      posts.append([company, location, title, link])
  except:
    pass
  print("remoteok :",len(posts))
  return posts

def scrape_page(page, search=""):
  if(page == "weworkremotely"):
    if (search ==""):
      return scrape_weworkremotely()
    return scrape_weworkremotely(search)
  elif(page == "stackoverflow"):
    if (search ==""):
      return scrape_stackoverflow()
    return scrape_stackoverflow(search)
  elif(page == "remoteok"):
    if (search ==""):
      return scrape_remoteok()
    return scrape_remoteok(search)
