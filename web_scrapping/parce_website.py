iimport requests
from bs4 import BeautifulSoup
import pprint
import json
import csv
import pandas as pd


path = "/Users/maximsukhoparov/Documents/Tim/программирование/web_scrapping/habr_vacancies.json"


def all_vacancies() -> dict:
    id = 1
    d1 = {}
    for page in range(1, 2):
        url = f"https://career.habr.com/vacancies?page={page}&salary=10000&type=all"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        box = soup.find_all("div", {"class": "vacancy-card__info"})

        for job in box:
            d1[id] = {}
            companies = (
                job.find("div", {"class": "vacancy-card__company"}).find("a").text
            )
            d1[id]["Company"] = companies

            vacancies = job.find("div", {"class": "vacancy-card__title"}).text
            d1[id]["Vacancy"] = vacancies

            salary = job.find("div", {"class": "basic-salary"}).text
            d1[id]["Salary"] = salary

            skills = job.find("div", {"class": "vacancy-card__skills"}).text.split(
                " • "
            )
            skillss = skills[1:]
            skils1 = ", ".join(skillss)
            d1[id]["Skills Required"] = skils1

            offon = job.find("div", {"class": "vacancy-card__meta"}).text.split(" • ")
            offon1 = ", ".join(offon)
            d1[id]["Remotion"] = offon1

            link = job.find("a", {"class": "vacancy-card__title-link"})["href"]
            url_text = f"https://career.habr.com/" + link
            response = requests.get(url_text)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.find("div", {"class": "collapsible-description__content"}).text
            d1[id]["Description"] = text

            id += 1

    return d1


"""
with open('habr__vacancies.csv', 'w') as f:
    for key in all_vacancies().keys():
        f.write("%s, %s\n" % (key, all_vacancies()[key]))
"""
df = pd.DataFrame.from_dict(all_vacancies())
df.to_csv(r"habr__vacancies.csv", index=False, header=True)

