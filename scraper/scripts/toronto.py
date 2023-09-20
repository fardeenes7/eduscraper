from bs4 import BeautifulSoup
import requests
import re
from scraper.models import University, Program


def get_programs():
    programs = []
    for i in range(0, 5):
        url = f"https://www.utoronto.ca/academics/programs-directory?field_program_type_target_id=6954&field_degrees_target_id=All&query=&page={i}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for program in soup.find("div", class_="view-content row").find_all("a"):
            url = program.get("href")
            programs.append(url)
    return programs


def get_program_details(program_url, university):
    page = requests.get(program_url)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        title = soup.find("h1", class_="page-title").text
        details = str(soup.find("article", class_="col-sm-8 order-2"))
        aside = str(soup.find("aside", 'col-sm-4 order-1'))
        degree = str(re.findall(r"<h3>Degrees Offered</h3>(.*?)<h3>", aside, re.DOTALL)[0])[1:]
        contact = str(re.findall(r"<h3>Contact &amp; Address</h3>(.*?)</aside>", aside, re.DOTALL)[0])[1:]
        program, created = Program.objects.get_or_create(title=title, university=university)
        program.url = program_url
        program.details = details
        program.degree = degree
        program.contact = contact
        program.save()
        print("Saved Successfully: ", program_url)
        return
    except Exception as e:
        print("Error Loading ", program_url,": ", e)
        return


def scrape():
    print("Scraping University of Toronto")
    university = University.objects.get(name="University of Toronto")
    programs = get_programs()
    for program in programs:
        get_program_details(program, university)

    print("Done scraping University of Toronto")
