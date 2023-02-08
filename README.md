# Plex Assets Exporter
Export posters, backgrounds, banners, and theme songs from Plex.

Note: Huge thanks to the maker of [Plex Poster Exporter](https://github.com/engelde/plex-poster-exporter). I got most of the code from there. 

I replaced username and password authentication with server url + authentication token for easier authentication (no need for 2FA). And I added support for Plex Meta Manager (PMM) overlays. By default the posters with an overlay won't be exported. This is because PMM will overlay the posters which will result in double overlays. Optionally you can still enable the export of posters with an overlay.

## Installation
```
sudo python3 -m pip install -r requirements.txt
```

## Usage
```
python3 Plex-Assets-Exporter.py --verbose
```

## Advanced Usage
```
python3 Plex-Assets-Exporter.py --serverurl "<SERVER URL>" --token "<PLEX TOKEN>" --library "<LIBRARY>" --assets "<ASSETS>" --overlays --overwrite --verbose
```

## Arguments

All arguments are optional. If one is required and it is not provided, the script will ask you to enter it.

| Option          | Description                                                                    | Default       |  
| --------------- | ------------------------------------------------------------------------------ | ------------- |  
| --serverurl     | The Plex server URL.                                                           |               |  
| --token         | The [Plex authentication token / X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).                                  |               |  
| --library       | The Plex library name.                                                         |               |  
| --assets        | Which assets should be exported? (all, posters, backgrounds, banners, themes)  |               |
| --overlays      | Export posters with overlay from Plex Meta Manager?                            | False         |  
| --overwrite     | Overwrite existing assets?                                                     | False         |  
| --verbose       | Show extra information?                                                        | False         |  
| --help          | Show the help message and exit.                                                |               |  

## Notes

This script expects all of your media files to be in the correct folder structure for Plex. If your files are not organized in the way that Plex recommends, you **will not** be able to use this.

[Movies](https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/)  
[Series](https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/)  

Enjoy!
