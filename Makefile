download:
	yes | python3 src/get_data.py

clean:
	rm -rf resampled_data/

login:
	copernicusmarine login	# Set up your credentials for the Copernicus Marine Service

resample:
	python3 src/resample_raster.py