import Grassdor_scraper as gs
import pandas as pd

path = "D:/MY IT/MachineLearning/job_salary_pred/chromedriver.exe"

df = gs.get_jobs('data scientist', 15, True, path)