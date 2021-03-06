ripsoup
=======

soup.io is shutting down, this time for real. Get your soup while it's coolign down rapidly and about to be sucked into
a black hole, there's a good internet citizen.

Read first: Caveats
-------------------

- The best way to export your soup is to use [this exporter](https://github.com/neingeist/soup-backup/) with your secret RSS feed.
- If you want to export a soup that is not yours (or if you've lost access to yours), this script is for you.
- If your soup is very large, your RSS feed may consistently time out or error, and you'll want to fall back to this
  script, too.
- As most exporters, this script only retrieves image files (including gifs), no videos or text posts. Sorry bout that.
  Pull Requests welcome if you make them in the next days.
- The soup has to be in pagination mode. No endless scrolling for this exporter, mouse wheels are expensive.
- Images are downloaded as-is, with no reference to timing. You'll end up with a lot of images, but not enough metadata
  to reconstruct the chronology of your soup.
- To avoid overloading soup.io, the URL collection script uses exponential backoff and can be slow. Don't be a jerk and
  hammer their servers. Please also use the recommended `-w2` option with wget for some space between file downloads.
- For a more complete single-step downloader with video and metadata support, please head over to
  [schlabber](https://github.com/Blickfeldkurier/schlabber).

Usage
-----

Make a Python virtualenv, and install

```
pip install -r requirements.txt
```

Run the script with your soup of choice:

```
python ripsoup.py myawesomesoupname
```

Once it's done, go to `data/myawesomesoupname` and run

```
wget -nc -w2 -i image_urls
```

and wait in happy trepidation. Will you make it before time runs out?
