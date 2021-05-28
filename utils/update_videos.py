# Retrieve the authenticated user's uploaded videos.
# Sample usage:
# python my_uploads.py

import argparse
import os
import re
import sys
import json

import httplib2

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from oauth2client.client import flow_from_clientsecrets


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def parse_description(description):
  my_json_text = re.findall("\{(?:[^{}]|)*\}", description)[0]
  my_json_json = json.loads(my_json_text)
  return my_json_json



# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(API_SERVICE_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))


def get_my_uploads_list():
  # Retrieve the contentDetails part of the channel resource for the
  # authenticated user's channel.
  channels_response = youtube.channels().list(
    mine=True,
    part='contentDetails'
  ).execute()

  for channel in channels_response['items']:
    # From the API response, extract the playlist ID that identifies the list
    # of videos uploaded to the authenticated user's channel.
    return channel['contentDetails']['relatedPlaylists']['uploads']

  return None

def list_my_uploaded_videos(uploads_playlist_id):
  videos = {}
  # Retrieve the list of videos uploaded to the authenticated user's channel.
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_playlist_id,
    part='snippet',
    maxResults=5
  )

  #print('Videos in list %s' % uploads_playlist_id)
  while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    # Print information about each video.
    for playlist_item in playlistitems_list_response['items']:
      video_id = playlist_item['snippet']['resourceId']['videoId']
      description = playlist_item['snippet']['description']
      json_description = parse_description(description)

      if json_description["id"][1:] in videos.keys():
        video = videos[json_description["id"][1:]]
      else:
        video = {}

      video["idString"] = str(json_description["id"][1:])
      video["id"] = int(json_description["id"][1:])
      video["channelId"] = 11249217 # jakenbakeLIVE
      video["channelName"] = json_description["uploader"]
      video["chapters"] = []
      video["chatEmbed"] = 0
      video["chatFile"] = None
      video["chatVideoFile"] = None
      video["created"] = json_description["timestamp"]
      video["length"] = json_description["duration"]
      video["metadataFile"] = None
      video["muteList"] = ""
      video["thumbnailUrl"] = ""
      video["title"] = json_description["fulltitle"]
      video["videoFile"] = None
      video["vodId"] = int(json_description["id"][1:])



      if json_description["vod_type"] == "raw":
        video["videoYoutubeId"] = video_id
      elif json_description["vod_type"] == "chat_only":
        #print(json_description["vod_type"])
        #print(json_description["id"])
        video["chatYoutubeId"] = video_id


      videos[json_description["id"][1:]] = video
      #print('(%s) \n %s' % (video_id, description))

    playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)

  for vid in videos:
    vid_array = []
    vid_array.append(videos[vid])
    #print(videos[vid])
    with open("../src/assets/video/" + vid + ".json", "w", encoding="utf-8") as f:
      json.dump(vid_array, f, ensure_ascii=False, indent=4)

  vid_array = []
  for vid in videos:
    vid_array.append(videos[vid])

  with open("../src/assets/videos/jakenbakeLIVE.json", "w", encoding="utf-8") as f:
    json.dump(vid_array, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
  args = argparser.parse_args()
  youtube = get_authenticated_service(args)
  try:
    uploads_playlist_id = get_my_uploads_list()
    if uploads_playlist_id:
      list_my_uploaded_videos(uploads_playlist_id)
    else:
      print('There is no uploaded videos playlist for this user.')
  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
