from flask_sqlalchemy import SQLAlchemy
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

db = SQLAlchemy()

# a recipe table

class Recipe(db.Model):
    """a recipe"""
    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_url = db.Column(db.String(600), nullable=False)
    recipe_title = db.Column(db.String(500), nullable=False)
    recipe_source = db.Column(db.String(128), nullable=True)
    recipe_ingredients = db.Column(db.TEXT, nullable=False)
    recipe_directions = db.Column(db.TEXT)
    recipe_tags = db.relationship("Tag",
                            secondary="tagrecipes", backref="recipes")

    def __repr__(self):
        """show helpful parts of recipe object"""
        return "<Recipe recipe_title=%s recipe_source=%s recipe_ingredients=%s recipe_directions=%s>" % (self.recipe_title,
                                               self.recipe_source, self.recipe_ingredients, self.recipe_directions)


class TagRecipes(db.Model):
    """tag recipe association table"""
    __tablename__ = "tagrecipes"

    tagrecipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # user_id = db.Column(db.ForeignKey('users.user_id'))
    tag_id = db.Column(db.ForeignKey('tags.tag_id'))
    recipe_id = db.Column(db.ForeignKey('recipes.recipe_id'))


    def __repr__(self):
        """show helpful parts of recipe object"""
        return "<TagRecipe tagrecipe_id=%s recipe_id=%s tag_id=%s>" % (self.tagrecipe_id,
                                               self.recipe_id, self.tag_id)



# a table of tags

class Tag(db.Model):
    """Restrictions for diets"""
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(128), nullable=True)
    recipe = db.relationship("Recipe",
                         secondary="tagrecipes",
                         backref="tags")


# class RecipeRatings(db.Model):
#     """Rating recipe association table"""
#     __tablename__ = "reciperatings"

#     reciperating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     recipe_id = db.Column(db.ForeignKey('recipes.recipe_id'))
#     rating_id = db.Column(db.ForeignKey('ratings.rating_id'))

# a table of recipe ratings 

class Rating(db.Model):
    """Rating a recipe"""
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rating_score = db.Column(db.Integer, nullable=True)
    recipe_id = db.Column(db.ForeignKey('recipes.recipe_id'))
    user_id = db.Column(db.ForeignKey('users.user_id'))
    recipe = db.relationship("Recipe",backref="recipes")
    user = db.relationship("User",backref="users")

# class UserRatings(db.Model):
#     """An association table for ratings and users"""
#     __tablename__ = "userratings"

#     userrating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.ForeignKey('users.user_id'))
#     rating_id = db.Column(db.ForeignKey('ratings.rating_id'))

# a user table 

class User(db.Model):
    """A user"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(80), nullable=True)
    name = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    restrictions = db.Column(db.String(60), nullable=True)



def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":


    from server import app
    connect_to_db(app)
    print "Connected to DB."

