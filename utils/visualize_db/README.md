# Visualize the QAlert 311 request db
The visuzlize_db notebook allows to easily visualize the geospatial data which is in the QAlert db.

Before running the notebook, install the python packages in the requirements.txt file.

NOTE: The notebook works by connecting to the qalert database within a running PostGIS instance, so you will need to ensure that the connection credentials in the 3rd cell are correct.

Once everything is installed and configured correctly, simply run all the cells. 
The final cell will output an interactive map with markers for each QAlert 311 request in the database.