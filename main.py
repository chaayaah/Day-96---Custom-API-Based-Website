from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import requests


from forms import CoordinatesForm, RandomUserForm, DogsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test123'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_api.db'
db = SQLAlchemy()
db.init_app(app)
Bootstrap5(app)

# CONFIGURE TABLES
class WeatherPost(db.Model):
    __tablename__ = "weathers"
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.String(250), nullable=False)
    feels_like = db.Column(db.String(250), nullable=False)
    temp_min = db.Column(db.String(250), nullable=False)
    temp_max = db.Column(db.String(250), nullable=False)
    pressure = db.Column(db.String(250), nullable=False)
    sea_level = db.Column(db.String(250), nullable=False)
    grnd_level = db.Column(db.String(250), nullable=False)
    humidity = db.Column(db.String(250), nullable=False)
    temp_kf = db.Column(db.String(250), nullable=False)
    weather_name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    icon = db.Column(db.String(250), nullable=False)
    clouds = db.Column(db.String(250), nullable=False)
    wind_speed = db.Column(db.String(250), nullable=False)
    wind_deg = db.Column(db.String(250), nullable=False)
    wind_gust = db.Column(db.String(250), nullable=False)
    city_name = db.Column(db.String(250), nullable=False)
    coordinate_lat = db.Column(db.String(250), nullable=False)
    coordinate_lon = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    timezone = db.Column(db.String(250), nullable=False)

class CoordinatesPost(db.Model):
    __tablename__ = "coordinates"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(250), nullable=False)
    lon = db.Column(db.String(250), nullable=False)

class RandomUserPost(db.Model):
    __tablename__ = "random_users"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.String(250), nullable=False)
    age = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(250), nullable=False)
    cell = db.Column(db.String(250), nullable=False)
    valid_id = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

class DogPost(db.Model):
    __tablename__ = "dogs"
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    bred_for = db.Column(db.String(250), nullable=False)
    breed_group = db.Column(db.String(250), nullable=False)
    life_span = db.Column(db.String(250), nullable=False)
    temperament = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_data():
    weather_result = db.session.execute(db.Select(WeatherPost))
    random_user_result = db.session.execute(db.Select(RandomUserPost))
    dog_result = db.session.execute(db.Select(DogPost))

    weather_post = weather_result.scalars().all()
    random_user_post = random_user_result.scalars().all()
    dog_post = dog_result.scalars().all()
    return render_template('index.html', all_weather_post=weather_post, all_random_user_post=random_user_post,
                           all_dog_post=dog_post)

@app.route('/weather', methods=["GET", "POST"])
def weather():
    form = CoordinatesForm()
    if form.validate_on_submit():
        weather_api_key = '976465b9d36b99d7b6e4823a4fb58daa'
        weather_endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
        weather_params = {
            "lat": form.lat.data,
            "lon": form.lon.data,
            "appid": weather_api_key,
            "cnt": 1
        }
        response = requests.get(weather_endpoint, params=weather_params)
        weather_data = response.json()
        new_post = WeatherPost(
            temp=weather_data['list'][0]['main']['temp'],
            feels_like = weather_data['list'][0]['main']['feels_like'],
            temp_min = weather_data['list'][0]['main']['temp_min'],
            temp_max = weather_data['list'][0]['main']['temp_max'],
            pressure = weather_data['list'][0]['main']['pressure'],
            sea_level = weather_data['list'][0]['main']['sea_level'],
            grnd_level = weather_data['list'][0]['main']['grnd_level'],
            humidity = weather_data['list'][0]['main']['humidity'],
            temp_kf = weather_data['list'][0]['main']['temp_kf'],

            weather_name = weather_data['list'][0]['weather'][0]['main'],
            description = weather_data['list'][0]['weather'][0]['description'],
            icon = weather_data['list'][0]['weather'][0]['icon'],

            clouds = weather_data['list'][0]['clouds']['all'],

            wind_speed = weather_data['list'][0]['wind']['speed'],
            wind_deg = weather_data['list'][0]['wind']['deg'],
            wind_gust = weather_data['list'][0]['wind']['gust'],

            city_name = weather_data['city']['name'],
            coordinate_lat = weather_data['city']['coord']['lat'],
            coordinate_lon = weather_data['city']['coord']['lon'],
            country = weather_data['city']['country'],
            population = weather_data['city']['population'],
            timezone = weather_data['city']['timezone'],
        )
        db.session.add(new_post)
        db.session.commit()
        last_post = db.session.query(WeatherPost).order_by(WeatherPost.id.desc()).first()
        return render_template("weather.html", form=form, last_post=last_post)
    last_post = db.session.query(WeatherPost).order_by(WeatherPost.id.desc()).first()
    return render_template("weather.html", form=form, last_post=last_post)

@app.route('/random_user', methods=['POST', 'GET'])
def random_user():
    form = RandomUserForm()
    if form.validate_on_submit():
        random_user_endpoint = 'https://randomuser.me/api/'
        response = requests.get(random_user_endpoint)
        result = response.json()

        title_name = result['results'][0]['name']['title']
        first_name = result['results'][0]['name']['first']
        last_name = result['results'][0]['name']['last']

        street_number = result['results'][0]['location']['street']['number']
        street_name = result['results'][0]['location']['street']['name']
        city = result['results'][0]['location']['city']

        state = result['results'][0]['location']['state']
        country = result['results'][0]['location']['country']
        postcode = result['results'][0]['location']['postcode']

        coordinates_lat = result['results'][0]['location']['coordinates']['latitude']
        coordinates_lon = result['results'][0]['location']['coordinates']['longitude']
        timezone_offset = result['results'][0]['location']['timezone']['offset']
        timezone_description = result['results'][0]['location']['timezone']['description']

        valid_id_name = result['results'][0]['id']['name']
        valid_id_value = result['results'][0]['id']['value']

        picture_large = result['results'][0]['picture']['large']
        picture_medium = result['results'][0]['picture']['medium']
        picture_thumbnail = result['results'][0]['picture']['thumbnail']

        new_random_user = RandomUserPost(
            gender = result['results'][0]['gender'],
            name = str(title_name + " " + first_name + " " + last_name),
            location=(str(street_number) + ", " + str(street_name) + ", " + str(city) + " City, " +
                      str(state) + ", " + str(country) + ", Postcode: " + str(postcode) + ", Lat:" + str(
                        coordinates_lat) +
                      ", Lon:" + str(coordinates_lon) + ", Timezone: " + str(timezone_offset) + ", " + str(
                        timezone_description)),
            username= result['results'][0]['login']['username'],
            password = result['results'][0]['login']['password'],
            date_of_birth= str(result['results'][0]['dob']['date']),
            age = str(result['results'][0]['dob']['age']),
            phone= str(result['results'][0]['phone']),
            cell = str(result['results'][0]['cell']),
            valid_id = (str(valid_id_name) + ", " + str(valid_id_value)),
            img_url = (str(picture_large) + ", " + str(picture_medium) + ", " + str(picture_thumbnail))
        )
        db.session.add(new_random_user)
        db.session.commit()
        result = db.session.execute(db.select(RandomUserPost))
        last_post = db.session.query(RandomUserPost).order_by(RandomUserPost.id.desc()).first()
        return render_template("random_user.html", form=form, last_post=last_post)
    last_post = db.session.query(RandomUserPost).order_by(RandomUserPost.id.desc()).first()
    return render_template("random_user.html", form=form, last_post=last_post)


@app.route('/dogs', methods=['POST', 'GET'])
def dogs():
    form = DogsForm()
    if form.validate_on_submit():
        dog_endpoint = "https://api.thedogapi.com/v1/images/search"
        dog_headers = {
            'x-api-key': 'live_coc1B5XGfjg3uUpvlRGFZm3R47DNdpLp3WMF2LEJn9ryEN5XIOIZZg1s0p8qgBxs'
        }
        dog_params = {
            'size': 'med',
            'mime_types': 'jpg',
            'format': 'json',
            'has_breeds': 'true',
            'order': 'RANDOM',
            'page': 0,
            'limit': 1
        }
        response = requests.get(dog_endpoint, headers=dog_headers, params=dog_params)
        result = response.json()
        new_dog = DogPost(
            weight=result[0]['breeds'][0]['weight']['metric'],
            height = result[0]['breeds'][0]['height']['metric'],
            name = result[0]['breeds'][0]['name'],
            bred_for = result[0]['breeds'][0]['bred_for'],
            breed_group = result[0]['breeds'][0]['breed_group'],
            life_span = result[0]['breeds'][0]['life_span'],
            temperament = result[0]['breeds'][0]['temperament'],
            url = result[0]['url']
        )
        db.session.add(new_dog)
        db.session.commit()
        last_post = db.session.query(DogPost).order_by(DogPost.id.desc()).first()
        return render_template("dogs.html", form=form, last_post=last_post)
    last_post = db.session.query(DogPost).order_by(DogPost.id.desc()).first()
    return render_template("dogs.html", form=form, last_post=last_post)

if __name__ == "__main__":
    app.run(debug=True)
