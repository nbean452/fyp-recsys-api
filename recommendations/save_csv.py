import os
from operator import itemgetter

import pandas as pd
from dotenv import load_dotenv
from supabase import Client, create_client

from recommendations.constants import compulsory_courses


def get_client():
    load_dotenv()

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_DB_ANON_KEY")
    supabase: Client = create_client(url, key)


def save_app_ratings():

    path = 'data/app_ratings.csv'

    compulsory_course_ids = []

    response = get_client().table("base_course").select(
        "id, code").order("id").execute()

    indices = []
    data = []

    for item in response.data:
        data.append(item.get("code"))
        indices.append(item.get("id"))

    query_pd = pd.DataFrame(data, index=indices, columns=['code'])

    # get compulsory course ids
    for course in compulsory_courses:
        compulsory_course_ids.append(
            query_pd.index[query_pd["code"] == course].values[0])

    # get data from db
    response = get_client().table("base_review").select(
        "*").order("id").execute()

    # create dataframe from the db response
    course_ratings = pd.DataFrame(response.data)

    # drop compulsory courses
    course_ratings = course_ratings[course_ratings["course_id"].isin(
        compulsory_course_ids) == False]

    # remove rest of the columns (optional)
    course_ratings.drop(
        columns=["id", "created_at", "comment", "updated_at"], inplace=True)

    course_ratings.to_csv(path, index=False)


def save_survey_results():
    path = 'data/survey_results.csv'

    response = get_client().table("base_course").select(
        "id, code").order("id").execute()

    indices = []
    data = []

    for item in response.data:
        data.append(item.get("code"))
        indices.append(item.get("id"))

    query_pd = pd.DataFrame(data, index=indices, columns=['code'])

    # get data from db
    response = get_client().table("survey").select(
        "*").order("id").execute()

    # create dataframe from the db response
    course_ratings = pd.DataFrame(response.data)

    # drop compulsory courses
    course_ratings = course_ratings[course_ratings.code.isin(
        compulsory_courses) == False]

    # change db response to fit data
    course_ratings.rename(
        columns={"session": "user_id", "id": "course_id"}, inplace=True)

    indices = []

    for index, row in course_ratings.iterrows():
        code, *rest = itemgetter('code', 'rating', 'user_id')(row)

        indices.append(query_pd.loc[query_pd['code']
                                    == code].index[0])

    course_ratings['course_id'] = indices

    # remove rest of the columns (optional)
    course_ratings.drop(
        columns=["created_at", "code"], inplace=True)

    unique_responses = course_ratings["user_id"].unique()

    for index, user_id in enumerate(unique_responses):
        # data from user survey is given id #9999 onwards
        course_ratings.loc[course_ratings["user_id"]
                           == user_id, "user_id"] = index + 9999

    course_ratings.to_csv(path, index=False)
