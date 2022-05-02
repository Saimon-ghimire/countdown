# import time
# import datetime
# from datetime import datetime
# now1=today.strftime('We are the %d, %b %Y')
# now=datetime.now("%Y %B %d")
# print(now)

# import datetime
# a=f"{datetime.datetime.now():%Y %B %d || %H:%M:%S}"
# print(a)
from datetime import datetime, timezone
now=datetime.now()
now=now.replace(tzinfo=timezone.utc)
print(now.strftime('%Y:%B'))