# Imports the create_app function from the website folder/package
from website import create_app

# create_app function creates flask app instance
# flask app runs in debug mode, which can provide error messages when bug is found
if __name__ == "__main__":
    app = create_app() 
    app.run(debug=True, host="0.0.0.0", port=5000) 