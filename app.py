# # This codebase is a rework of an original I worked on that pulled the data from the census, manually transformed it,
# # and stored it in excel. This new code gets user input for census acs years, pulls the data,
# # transforms with pandas, and saves to GSheets. With Tableau public (not desktop!),
# # you can have your data automatically sync (every 24 hours it updates but can be done manually if needed sooner).
# # The goal here was to make things as hands off for the client as they aren't very technically proficient.
# # For questions, comments, concerns email taymal1987@gmail.com
import requests
import config
import pygsheets
import pandas as pd
import os
import json
import us
from dotenv import load_dotenv
from flask import Flask, abort, request, render_template
from params import Params
from census import Census
from google import Google

load_dotenv()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('dashboard.html')

@app.route('/year-select', methods=['GET'])
def dashboard():
    return render_template('index.html')

@app.route('/update_gsheet', methods=['GET'])
def update_sheet():
    params = Params()
    census = Census()
    google  = Google()

    data = request.args
    acs_year = str(data['year'])
    params.pword_validate(str(data['pword']))
    acs_year = int(data['year']) #as int for validation
    params.year_validate(acs_year)
    acs_year = str(acs_year) #as string for concatentation in query string

    api =  google.auth('FLASK_ENV')
    wb = google.open_workbook(api, 'FLASK_ENV')
    
    API_KEY = census.get_census_api_key()
    URL = 'https://api.census.gov/data/'
    YEAR = acs_year + '/'
    DATA_SET = 'acs/acs5'
    BASE_URL = URL + YEAR + DATA_SET
    GET = '?get='
    GROSS_RENT_PERCENT_INCOME_25_30 = 'B25070_006E'
    GROSS_RENT_PERCENT_INCOME_30_34 = 'B25070_007E'
    GROSS_RENT_PERCENT_INCOME_35_39 = 'B25070_008E'
    GROSS_RENT_PERCENT_INCOME_40_49 = 'B25070_009E'
    GROSS_RENT_PERCENT_INCOME_50_PLUS = 'B25070_010E'
    TOTAL_POPULATION_BURDENED = 'B25070_001E'
    MED_INCOME = 'B06011_001E'


    COMMA = ','
    FOR = '&for='
    IN = '&in='
    ALL_STATES = 'state:*'
    ALL_COUNTY = 'county:*'

    # FINAL_URL = https://api.census.gov/data/2018/acs/acs5?get=B25070_010E&for=county:*&in=state:*
    # this string will get the population of individuals that pay 30 - 50% of their income
    # in rent for all counties in in all state throughout the US.
    FINAL_URL = BASE_URL \
        + GET + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
        + GROSS_RENT_PERCENT_INCOME_25_30 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_40_49 + COMMA\
        + TOTAL_POPULATION_BURDENED\
        + FOR + ALL_COUNTY\
        + IN + ALL_STATES

    r = requests.get(url=FINAL_URL + API_KEY)
    # values is the return value from the census  API
    values = r.json()
    df = pd.DataFrame(values)
    #headers for df
    df.columns = ['GROSS_RENT_PERCENT_INCOME_50_PLUS', 'GROSS_RENT_PERCENT_INCOME_25_30', 'GROSS_RENT_PERCENT_INCOME_30_34',
                  'GROSS_RENT_PERCENT_INCOME_35_39', 'GROSS_RENT_PERCENT_INCOME_40_49', 'TOTAL_POPULATION_BURDENED', 'state fips', 'county fips']

    df.drop([0], inplace=True)

    #compute burdening, convert to decimal, round to 4 sig fig
    df['PERCENT RENT BURDENED'] = (((pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_25_30']) + pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_30_34']) + pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_35_39']) + pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_40_49'])) / pd.to_numeric(df['TOTAL_POPULATION_BURDENED'])) * 100).round(4)
    df['PERCENT SEVERLY RENT BURDENED'] = ((pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_50_PLUS']) / pd.to_numeric(df['TOTAL_POPULATION_BURDENED']))*100).round(4)

    df['fips'] = df['state fips'] + df['county fips']
    df['state'] = df['state fips'].apply(lambda x: us.states.lookup(x)) #state name from us lib

    df.dropna(inplace=True)

    sheet = google.worksheet_by_title_wrapper(wb, 'viz burden data')
    google.clear_wrapper(sheet)
    google.set_dataframe_wrapper(sheet, df, (1, 1))
    return 'ayyyyy'

if __name__ == '__main__':
    app.run()
