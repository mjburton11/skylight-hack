import json
import os
import urllib.request

SKYLIGHT_TOKEN = os.environ["SKYLIGHT_TOKEN"]
FRAME_ID = os.environ.get("FRAME_ID", "3701822")
API_VERSION = "2026-02-01"

CHILDREN = {
    "lily":  "9480217",
    "james": "9480215",
    "jack":  "9480214",
}

def reward_points(child_id, points):
    url = f"https://app.ourskylight.com/api/frames/{FRAME_ID}/reward_points"
    data = json.dumps({
        "category_ids": [child_id],
        "points": points
    }).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {SKYLIGHT_TOKEN}",
        "Content-Type": "application/json",
        "skylight-api-version": API_VERSION,
    })
    with urllib.request.urlopen(req) as resp:
        return resp.status

def speak(text):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": text},
            "shouldEndSession": True
        }
    }

def handler(event, context):
    req_type = event["request"]["type"]

    if req_type == "LaunchRequest":
        return speak("Skylight ready. You can give or deduct points for Lily, James, or Jack.")

    if req_type != "IntentRequest":
        return speak("Sorry, I didn't understand that.")

    intent = event["request"]["intent"]
    intent_name = intent["name"]

    if intent_name in ("AMAZON.CancelIntent", "AMAZON.StopIntent"):
        return speak("Goodbye.")

    if intent_name not in ("GivePointsIntent", "DeductPointsIntent"):
        return speak("Sorry, I didn't understand that.")

    slots = intent.get("slots", {})
    child_name = slots.get("child", {}).get("value", "").lower()
    points_val = slots.get("points", {}).get("value")

    if child_name not in CHILDREN:
        return speak(f"I don't recognize the name {child_name}. You can reward Lily, James, or Jack.")

    try:
        points = int(points_val) if points_val else 1
    except ValueError:
        return speak("I didn't catch how many points. Please try again.")

    if intent_name == "DeductPointsIntent":
        points = -points

    child_id = CHILDREN[child_name]
    action = "deducted" if points < 0 else "gave"

    try:
        reward_points(child_id, points)
        return speak(f"{action.capitalize()} {abs(points)} point{'s' if abs(points) != 1 else ''} for {child_name.capitalize()}.")
    except Exception as e:
        print(f"Error calling Skylight API: {e}")
        return speak("Sorry, something went wrong contacting Skylight.")
