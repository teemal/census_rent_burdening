import os
import datetime
from flask import Flask, abort, request, redirect

class Params(object):
    def __init__(self):
        pass

    def pword_validate(self, pword):
        if str(pword) != str(os.getenv('PWORD')):
            return abort(403)
        return 'passed'

    def year_validate(self, year):
        """
        requires year of type int just for simple validation
        """
        now = datetime.datetime.now()
        if(type(year) != int):
            return abort(400)
        #oldest acceptable acs year is 2011, but validating with 2013 to maintain trends viz
        if int(year) > now.year - 1 or int(year) < 2013:
            return abort(422)
        return