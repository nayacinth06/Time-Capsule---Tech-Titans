# Time-Capsule---Tech-Titans
A digital time capsule webpage where users can create, store, and open personal messages for the future. Includes customizable background and SQLite for data storage.
Features:
Create a Time Capsule:

Users can write a personal message for their future selves.
They can select a date on which they wish to open the capsule.
The time capsule is saved in the database with a timestamp of creation and the specified open date.
View Existing Time Capsules:

Users can view a list of all their created time capsules along with the date they will be opened.
If the current date is the same as or later than the open date, users can open the capsule and read the stored message.
Time capsules that have been opened are deleted from the database.
Background Customization:

The app allows for a local background image to be set for the page to enhance the user experience. Users can provide an image file (such as a personal photo or a meaningful background) that is encoded and displayed as the app's background.
SQLite Database:

The project utilizes SQLite to manage and store time capsule data (message, open date, and creation timestamp).
The app uses SQLite queries to insert, retrieve, and delete records based on user interaction.
Technologies Used:
Streamlit: A Python framework for building interactive web apps.
SQLite: A lightweight, serverless database engine used to store time capsule data.
Pandas: For handling and querying data in a tabular format.
Python: The primary language used for backend logic and app functionality.
Base64: Used to encode and embed local images as the background for the app.
