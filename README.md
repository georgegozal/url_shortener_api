# Flask_URL_Shortener_API


# you can see my app on pythonanywhere
> http://g2gozal.pythonanywhere.com/

### GET https://base_url/<string>: "Redirects to the original URL
### POST https://base_url/: "Creates a shortened URL. Send data as JSON: {"url": "https://www.example.com"}

# Setup and Run
> git clone https://github.com/georgegozal/url_shortener_api.git

> cd Flask_URL_Shortener

> pip3 install -r requirements.txt

> python3 main.py

in web browser type:

> https://localhost:5000

# To run tests Run
> tox