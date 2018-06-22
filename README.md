<img width="80" src="docs/logo.svg" alt="Logo">

# product-release-notes

[![Build Status](https://travis-ci.org/nickromano/product-release-notes.svg?branch=master)](https://travis-ci.org/nickromano/product-release-notes)
[![Coverage Status](https://coveralls.io/repos/github/nickromano/product-release-notes/badge.svg?branch=master)](https://coveralls.io/github/nickromano/product-release-notes?branch=master)
[![PyPi](https://img.shields.io/pypi/v/product_release_notes.svg)](https://pypi.python.org/pypi/product-release-notes)
![PyPI](https://img.shields.io/pypi/pyversions/product_release_notes.svg)
![PyPI](https://img.shields.io/pypi/l/product_release_notes.svg)

Add a changelog for your website that includes release notes for each of your clients.

* Support for multiple clients (iOS, Android, Web)
* RSS feed of changes
* Easily extend the style of the page
* Automatically pull release notes from iTunes
* Automatically pull release notes from Google Play

You can either install it as a package into your existing project, or deploy directly to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

![Release Notes](docs/release-notes.png)

Edit releases using the Django Admin.

![Django Admin](docs/release-notes-editor.png)

## Examples

* [Pinnacle Climb Log](https://pinnacleclimb.com/release-notes/)
* [Echo Responder](https://echoresponder.com/release-notes/)

## Installation

1) Install the python package

```
pip install product_release_notes
```

2) Add `product_release_notes` to `INSTALLED_APPS` in your `settings.py`.

3) Add a url to your `urls.py`.

```python
# project.urls.py
from django.conf.urls import url, include

urlpatterns = [
    url(r'^release-notes/', include('product_release_notes.urls')),
]
```

4) Run migrations to create the release notes tables.

```
./manage.py migrate
```

## Settings

Optional settings to customize the release notes page.

```python
RELEASE_NOTES_PAGE_DESCRIPTION = 'My product updates.'
RELEASE_NOTES_AUTO_PUBLISH = False
```

5) Optional - Create release note drafts when new versions are released to iTunes

Fill in the `itunes_url` field when creating a client.

Add a scheduled job to run at least daily to check for new versions in iTunes and Google Play

```
./manage.py check_app_stores
```

6) Optional - Customize the release notes page

Create a template `release_notes/base.html` to override the packages base template.

```html
<!DOCTYPE html>
<html>
<head>
	<title>Release Notes</title>

	{% block release_notes_extra_head %}{% endblock %}
</head>
<body>

{% block release_notes_body_header %}{% endblock %}
{% block release_notes_body %}{% endblock %}

</body>
</html>
```
