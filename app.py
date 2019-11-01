from apps import app
import argparse
import os

# test
app.config.from_object(os.getenv("APP_SETTINGS"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
