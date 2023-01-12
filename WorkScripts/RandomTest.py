#from dateutil.relativedelta import relativedelta as reldate

import dateutil.relativedelta as reldate
import datetime

base_date = datetime.date.today()
three_mon_rel = reldate.relativedelta(months=3)

base_date = base_date + three_mon_rel

new_day = base_date.day
new_month = base_date.month
new_year = base_date.year