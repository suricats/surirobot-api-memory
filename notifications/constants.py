import timezonefinder as timezonefinder
from dateutil import tz

# Localisation of Paris for timezone
LATITUDE_DEFAULT = 48.8589506
LONGITUDE_DEFAULT = 2.276848
# Timezone
tf = timezonefinder.TimezoneFinder()
TZ_DEFAULT = tz.gettz(tf.timezone_at(lng=LONGITUDE_DEFAULT, lat=LATITUDE_DEFAULT))

google_sheet_service = None
GOOGLE_SHEET_SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SPREADSHEET_ID = '1KMWiuyVzWGx-GZD94utaGPCPRYtrLHdplH2UOb9q-U4'
RANGE_NAME = 'news!A2:B4'