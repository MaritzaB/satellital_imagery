download:
	yes | python3 src/get_data.py

clean:
	rm -rf resampled_data/

login:
	copernicusmarin login	# Set up your credentials for the Copernicus Marine Service
