import os
import sys

import findspark
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.sql import SparkSession, SQLContext

from recommendations.save_csv import save_app_ratings, save_survey_results


def save_model():
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    # init spark
    findspark.init()

    spark = SparkSession.builder\
        .master("local")\
        .appName("with-spark-recommender")\
        .getOrCreate()

    sc = spark.sparkContext
    sqlContext = SQLContext(sc)

    # get concatenated data from survey and app
    survey_ratings = pd.read_csv(
        'server_data/csv/survey_results.csv', index_col=False)
    app_ratings = pd.read_csv(
        'server_data/csv/app_ratings.csv', index_col=False)
    course_ratings = pd.concat([app_ratings, survey_ratings])

    course_ratings = sqlContext.createDataFrame(course_ratings)

    # create test and train set
    (train, test) = course_ratings.randomSplit([.8, .2])

    als = ALS(userCol="user_id", itemCol="course_id", ratingCol="rating",
              coldStartStrategy="drop", nonnegative=True)

    param_grid = ParamGridBuilder()\
        .addGrid(als.rank, [12, 13, 14])\
        .addGrid(als.maxIter, [2, 3, 4])\
        .addGrid(als.regParam, [.17, .18, .19])\
        .build()

    evaluator = RegressionEvaluator(
        metricName="rmse", labelCol='rating', predictionCol='prediction')

    cv = CrossValidator(
        estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=3)

    model = cv.fit(train)

    best_model = model.bestModel
    best_model.write().overwrite().save("server_data/model/")

# save data from survey and app ratings into csv, and then train the data!


def cron():
    save_survey_results()
    save_app_ratings()
    save_model()


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        cron,
        "interval",
        name="train model every hour",
        minutes=60
    )

    scheduler.start()
