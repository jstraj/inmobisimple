# inmobisimple

An unofficial python wrapper for Inmobi Publisher Reporting API. 
The API documentation can be found at https://support.inmobi.com/monetize/reporting-api/. 

## Getting Started


### Installation

inmobisimple is available on the Python Package Index (PyPI) at https://pypi.org/project/inmobisimple/0.1/

```
pip install inmobisimple
```

### Prerequisites

To use the Inmobi Publisher Reporting API, you need the following things:


* API Key ([Instructions](https://support.inmobi.com/monetize/reporting-api/reporting-api/))
* Username
* Password (optional)


### Examples

First, import the inmobisimple package and create an InmobiAuth object to generate session.

```python
from inmobisimple.inmobi import InmobiAuth

auth = InmobiAuth(username="rajat.panwar@example.com", secret_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
auth_session = auth.generate_session()

print(auth_session.account_id)
'4028cb************************14'
print(auth_session.session_id)
'b8************************d31942'
print(auth_session.username)
'rajat.panwar@example.com'
print(auth_session.secret_key)
'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

Now you have to save this session somewhere so that you can reuse it later. As per the documentation,

>A session is valid for 24 hours from the time of issue. An API key can be used to generate up to 15 valid sessions in 24 hours timeframe. 

Now that you the required Inmobi Session, you can now generate a report.
After creating the report you can fetch the results from it. 

```python

from inmobisimple.inmobi import Inmobi

inmobi = Inmobi(auth_session) # Creates an inmobi object

# required parameters for the API call
payload = {
    "reportRequest": {
        "metrics": ['adImpressions'],
        "groupBy": ['date','country'],
        "timeFrame": "{start_date}:{end_date}".format(start_date="2019-01-30", end_date="2019-01-31")
    }
}
report = inmobi.create_report(payload)

while report.has_next_page():
        # length param is optional. Default is 5000
        response = report.get_next_page(length=100)
        print(response)
```

The length parameter is optional. Default value is 5000.

### Pagination

For the most part pagination is handled by inmobisimple. But keep in mind that last result will always be empty and look like this:

```python
{'error': False, 'respList': []}
```

Even thought the Inmobi Publisher Reporting API recommends that
>Last such call should get rows less than or equal to “length”

But this way to test the last page is always error-prone because last page may have the same number of items as the provided page length.

I have implemented a different way to paginate the result set where last page is marked when the result set has length 0.


### More Usages


#### Reusing the generated session 

Saving the session in a file or db is a good practice because each session is valid for 24 hours and can be generated only 15 times in 24 hours.

You can always reconstruct the Auth object from session_id, account_id, secret_key and password (optional).

```python
from inmobisimple.models import Auth

auth = Auth(
        session_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        account_id="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
        username="rajat.panwar@example.com", #optional
        password=None, #optional
        secret_key="zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    )
```



You can also mention the Reporting API and Auth versions while making an API call.

#### Changing API Version

 ```python
from inmobisimple.inmobi import InmobiAuth, Inmobi

# Default Auth version is 1.0
auth = InmobiAuth(username="rajat.panwar@example.com", 
                secret_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                version='1.0')

# Default API Reporting version is 3.0
inmobi = Inmobi(auth, version='3.0')
```

#### Including Filters

You can include filters like mentioned in the api.
Just make the changes in the payload dict.

```python
payload = {
    "reportRequest": {
        "metrics": ['adImpressions'],
        "groupBy": ['date','country'],
        "timeFrame": "{start_date}:{end_date}".format(start_date="2019-01-30", end_date="2019-01-31"),
        "filterBy": [{ "filterName":"adImpressions", "filterValue": "300" , "comparator":">"}]
    }
}
```

#### More...

Check examples/ directory

## Contributing

Codes can never be perfect. Please feel free to notify me or submit pull requests if you think there are some bugs or the code needs some kind of improvement.

## License

This project is licensed under the GNU GPL v3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
