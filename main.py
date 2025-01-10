from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_ckeditor import CKEditor
from werkzeug.utils import redirect
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)


# Form base
class CreateACoffee(FlaskForm):
    name = StringField("Name of the Coffee", validators=[DataRequired()])
    map_url = StringField("Url For the location", validators=[DataRequired()])
    img_url = StringField("Url to add an image", validators=[DataRequired()])
    location = StringField("Where is the coffee shop?", validators=[DataRequired()])
    has_sockets = BooleanField("Does the coffee has electric cockets for the clients?", validators=[DataRequired()])
    has_toilets = BooleanField("Does the coffee have bathroom?", validators=[DataRequired()])
    has_wifi = BooleanField("Wi-fi access?", validators=[DataRequired()])
    seats = StringField("How many seats?", validators=[DataRequired()])
    coffee_price = StringField("Avarage coffee price?", validators=[DataRequired()])
    submit = SubmitField("Add coffee to our data base")

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# base table for the coffee's list
class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)



with app.app_context():
    db.create_all()

print(app.config['SQLALCHEMY_DATABASE_URI'])


@app.route("/")
def home():
    form = CreateACoffee()
    if form.validate_on_submit():
        new_coffee = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilets=form.has_toilets.data,
            has_wifi=form.has_wifi.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_coffee)
        db.session.commit()
        return redirect(url_for("home"))
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    for cafe in cafes:
        print(cafe.name, cafe.location, cafe.coffee_price)
    return render_template("index.html", coffee_list=cafes, form=form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(Cafe, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
