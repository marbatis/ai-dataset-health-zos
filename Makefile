

# ---- RAT helpers ----
rat-setup:
	pip install -r requirements-extra.txt

rat-notebooks: rat-setup
	jupyter notebook notebooks/10_ALOS2_seasonal_composites.ipynb

rat-notebooks-all: rat-setup
	jupyter notebook notebooks/10_ALOS2_seasonal_composites.ipynb notebooks/11_GEDI_L4C_WSCI_extraction.ipynb


# ---- Pre-commit helpers ----
precommit-install:
	pre-commit install

precommit-run:
	pre-commit run --all-files
