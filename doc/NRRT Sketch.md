# NRRT Sketch

Here is my sketch for the NRRT / onesto app. I thought I would use notion as I haven't used this before! It seems like a nice tool! 🙂 

I've captured these initial ideas at [https://github.com/WeakLemonDrink/nrrt_project](https://github.com/WeakLemonDrink/nrrt_project) if you want to have a look. In particular, have a look at [https://github.com/WeakLemonDrink/nrrt_project/blob/master/models.py](https://github.com/WeakLemonDrink/nrrt_project/blob/master/models.py) which shows you how the Django models that define db tables would work.

# Overall app architecture

So the app needs to have:

- A method to upload and create abstract models via csv or json
- A method to upload and create instances linked to abstract models
- Methods to process and store incoming instances and abstract models
- A method to retrieve data via json

I think the easiest way to implement the needs above is to develop a [Django](https://www.djangoproject.com/) app, including using [Django Rest Framework](https://www.django-rest-framework.org/) to provide a simple API. This will provide us with the endpoints we need to upload, view and retrieve data and also provide methods to serialize/deserialize data without writing too much custom code ourselves. Initially we don't need to deploy the developed app on the internet, we can just develop it and run it individually as [localhost](http://localhost). It would be very simple to deploy it to either AWS or [Heroku](https://www.heroku.com/) though if you want.

To store the abstract model and instance data and allow filtering and searching, I do think creating a database for this is the right way to start. Django provides a python abstraction layer around the database, so everything is defined in python. This doesn't mean you can't use raw SQL if you want to, but most operations can be done using python which makes it really useful when writing functions to upload, process and download data. The database could be in PostgreSQL, or even sqlite to make it easier. 

## Database tables

From looking at your data examples I would initially create db tables using [Django models](https://docs.djangoproject.com/en/3.1/topics/db/models/) to capture abstract base model and instance data like this:

![NRRT%20Sketch%20984b49bf981b4330ad40979f41678d15/db_tables2.png](NRRT%20Sketch%20984b49bf981b4330ad40979f41678d15/db_tables2.png)

This would allow you to store and filter data easily. Methods could be linked to table definition to deserialize and serialize the data when uploading and downloading. You could then create many ABM db entries with the same name, and have many-to-one relationships to define the attributes, measures and links associated with each ABM entry.

Instance data would mostly be defined by the ABM. All other common fields like id etc would be created by the [django.db.models.model](https://docs.djangoproject.com/en/3.1/topics/db/models/) inheritance.

## Upload

I would create two upload methods, `upload_abm` to create ABM entries, and `upload_instance` to create Instance entries. Initially I would write simple [Django views](https://docs.djangoproject.com/en/3.1/topics/http/views/) to do this, linked to endpoints like:

```jsx
http://localhost:8000/abm
http://localhost:8000/instance
```

This endpoint, url etc would all be provided by Django code, so would be quick to set up. Both upload functions would validate and then process the incoming data, before storing it to new AbstractBaseModel or Instance entries. In order to upload data, you would just have to do a post request with the data you are uploading, [here is an example](https://requests.readthedocs.io/en/master/user/quickstart/).

To begin with these would be very simple methods. For future work, these methods could be extended to provide authentication, form based input using a browser, automated scraping and population etc. All this could be done using Django and Django Rest Framework.

## View and retrieve

To view and retrieve the data that is stored in the databases, I would use Django Rest Framework again using the endpoints above. By performing a http get request like this again using requests:

```python
import requests

>>> r = requests.get('[http:](https://api.github.com/events)//localhost:8000/abm?format=json')
>>> r.text
```

This would provide you with a full json output of the data. As the data grows, Django Rest Framework provides pagination so the returned data isn't too large. Django Rest Framework also provides ways to filter returned results using querystrings, like this:

```python
import requests

>>> r = requests.get('http://localhost:8000/abm?name=book&format=json')
>>> r.text
```

Or using the id directly like this:

```python
import requests

>>> r = requests.get('http://localhost:8000/abm/1')
>>> r.text
```

This would allow you quickly get the information you need. The data returned would be serialized to json in the format you have defined in your examples. If you wanted a web based view this could be done using the Django template engine and putting the data in a folder tree as you suggested in our call, or in a table format.

## The Node Relationship Ranking Table (NRRT)

My understanding is that the NRRT is a table of ranking clusters. A ranking cluster is a unique combination of a named item (e.g. "Book", "Car" etc.), a relationship (e.g.  "(Book)<-[WROTE]-(Person)") and some sort of search term. The app would create these tables dynamically using field data from ranking cluster entries, and either render them on the app or make them available to download via csv. I think this should be fine when the amount of data being used by the app is small to medium, but tables may need to be generated automatically and cached if data sets get large in the future.