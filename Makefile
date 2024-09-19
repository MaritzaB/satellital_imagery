download: login
	yes | python3 src/get_data.py

clean:
	rm -rf resampled_data/
	rm -rf src/__pycache__/

include .env
export $(shell sed 's/=.*//' .env)
login:
	@echo "Logging in to Copernicus Marine Service"
	copernicusmarine login

resample:
	python3 src/resample_raster.py
