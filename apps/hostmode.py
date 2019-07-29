import argparse

ap = argparse.ArgumentParser()
ap.add_argument(
    "-hm", "--hostmode", required=False, help="localserver mode or production mode"
)
args = vars(ap.parse_args())

