PLUGIN_PREFIX = '/video/disney'
NAME = 'Disney'
JSON_URL = 'http://video.disney.com/_grill/json/'
SHOWS_URL = JSON_URL + '%s/all'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME

####################################################################################################
@handler(PLUGIN_PREFIX, NAME)
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(Shows, title="Shows",group='shows'), title="Shows"))
	oc.add(DirectoryObject(key=Callback(Shows, title="Collections",group='collections'), title="Collections"))

	return oc

####################################################################################################
@route(PLUGIN_PREFIX + '/shows')
def Shows(title, group):

	oc = ObjectContainer(title2 = title)
	json = JSON.ObjectFromURL(SHOWS_URL % group)

	for show in json['stack'][0]['data']:
		title = show['title']

		try: summary = show['description']
		except:
			try: summary = show['short_desc']
			except: summary = ''

		try: thumb = show['logo']
		except:
			try: thumb = show['square2x']
			except:
				try: thumb = show['square']
				except: continue
				# shows without icons seem not to have any content either so,
				# no point adding them to the list

		url = show['href']

		oc.add(DirectoryObject(
			key = Callback(Videos, title=title, thumb=thumb, url=url),
			title = title,
			summary = summary,
			thumb = Resource.ContentsOfURLWithFallback(thumb)
		))

	return oc

####################################################################################################
@route(PLUGIN_PREFIX + '/videos')
def Videos(title, thumb, url):

	oc = ObjectContainer(title2=title)
	json_url = JSON_URL + url.split('video.disney.com/')[1]
	json = JSON.ObjectFromURL(json_url)

	for group in json['stack']:
		if group['type'] == 'video':
			for clip in group['data']:
				if 'Disney Junior' in title or 'Disney XD' in title:
					if "Live Stream" in clip['title']:
						continue
					if 'Disney' not in clip['ptitle']:
						clip_title = clip['ptitle'] + ' - ' + clip['title']
					else:
						clip_title = clip['title']
				else:
					clip_title = clip['title']

				summary = clip['description'] if 'description' in clip else None

				try:
					duration = int(clip['duration_sec'])*1000
				except:
					duration = None

				clip_thumb = clip['thumb']
				url = clip['href']

				oc.add(VideoClipObject(
					url = url,
					title = clip_title,
					summary = summary,
					duration = duration,
					thumb = Resource.ContentsOfURLWithFallback(clip_thumb)
				))

	return oc
