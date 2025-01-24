from flask import Flask, render_template
import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from threading import Lock, Event

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

# Set feature_dance_flag_key to the feature flag key you want to evaluate.
feature_dance_flag_key = "freeflag"
feature_music_flag_key = "musicflag"

# this is printed in the terminal 
def show_evaluation_result(key: str, value: bool):
    print()
    print(f"*** The {key} feature flag evaluates to {value}")

@app.route("/")
def home():
    # Set up the evaluation context
    context = Context.builder("example-user-key").kind("user").name("Sandy").build()

    # Check the value of the feature flag
    dance_flag_value = ldclient.get().variation(feature_dance_flag_key, context, False)
    music_flag_value = ldclient.get().variation(feature_music_flag_key, context, False)

    # Render different templates based on the flag value
    if dance_flag_value:
        # add another flag to insert a song file 
        return render_template("dance.html")
    if dance_flag_value and music_flag_value:
        return render_template("dance.html", playmusic = music_flag_value)
    else:
        return render_template("wait.html")

if __name__ == "__main__":
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not feature_dance_flag_key:
        print("*** Please set the LAUNCHDARKLY_FLAG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = \
        Context.builder('example-user-key').kind('user').name('Sandy').build()

    # Check the value of the feature flag.
    # check if the variable value names are correct

    dance_flag_value = ldclient.get().variation(feature_dance_flag_key, context, False)
    music_flag_value = ldclient.get().variation(feature_music_flag_key, context, False)

    show_evaluation_result(feature_dance_flag_key, dance_flag_value)
    show_evaluation_result(feature_music_flag_key, music_flag_value)
    
    try:
        app.run(debug=True)
        Event().wait()
    except KeyboardInterrupt:
        pass
