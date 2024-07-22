#Imports the create_app function from the website folder/package
from website import create_app

#
if __name__ == "__main__":
    app = create_app() # create_app function creates flask app instance
    app.run(debug=True) # flask app runs in debug mode, which can provide error messages when bug is found