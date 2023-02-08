#!/usr/bin/env python3

import os
import sys

# sys
sys.dont_write_bytecode = True
if sys.version_info[0] < 3:
    print('\033[91mERROR:\033[0m', 'you must be running python 3.0 or higher.')
    sys.exit()

# click
try:
    import click
except:
    print('\033[91mERROR:\033[0m', 'click is not installed.')
    sys.exit()

# plexapi
try:
    import plexapi.utils
    from plexapi.server import PlexServer, CONFIG
    from plexapi.exceptions import BadRequest
except:
    print('\033[91mERROR:\033[0m', 'plexapi is not installed.')
    sys.exit()

# defaults
NAME = 'Plex Assets Exporter'
VERSION = 0.1

# plex
class Plex():
    def __init__(self, serverurl=None, token=None, library=None, overwrite=False, verbose=False, overlays=False):
        self.serverurl = serverurl
        self.token = token
        self.server = ''
        self.libraries = []
        self.library = library
        self.overwrite = overwrite
        self.verbose = verbose
        self.overlays = overlays
        self.downloaded = 0
        self.skipped = 0

        self.getServer()
        self.getLibrary()


    def getServer(self):
        if self.serverurl == None:
            self.serverurl =  input("Enter your server URL: ")
        if self.token == None:
            self.token =  input("Enter your authentication token / X-Plex-Token: ")
        self.server = PlexServer(self.serverurl, self.token)  

    def getLibrary(self):
        self.libraries = [ _ for _ in self.server.library.sections() if _.type in {'movie', 'show'} ]
        if not self.libraries:
            print('\033[91mERROR:\033[0m', 'no available libraries.')
            sys.exit()
        if self.library == None or self.library not in [ _.title for _ in self.libraries ]:
            self.library = plexapi.utils.choose('Select library', self.libraries, 'title')
        else:
            self.library = self.server.library.section(self.library)
        if self.verbose:
            print('\033[94mSELECTED LIBRARY:\033[0m', self.library.title)

    def getLibraryItems(self):
        if self.overlays:
            return self.library.all()
        else:
            return self.library.search(filters={"label!": "Overlay"})

    def getPath(self, item, season=False):
        if self.library.type == 'movie':
            for media in item.media:
                for part in media.parts:
                    return part.file.rsplit('/', 1)[0]
        elif self.library.type == 'show':
            for episode in item.episodes():
                for media in episode.media:
                    for part in media.parts:
                        if season:
                            return part.file.rsplit('/', 1)[0]
                        return part.file.rsplit('/', 2)[0]

    def download(self, url=None, filename=None, path=None):
        if not self.overwrite and os.path.isfile(path+'/'+filename):
            if self.verbose:
                print('\033[93mSKIPPED:\033[0m', path+'/'+filename)
            self.skipped += 1
        else:
            if plexapi.utils.download(self.server._baseurl+url, token, filename=filename, savepath=path):
                if self.verbose:
                    print('\033[92mDOWNLOADED:\033[0m', path+'/'+filename)
                self.downloaded += 1
            else:
                print('\033[91mDOWNLOAD FAILED:\033[0m', path+'/'+filename)
                sys.exit()

# main
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(prog_name=NAME, version=VERSION, message='%(prog)s v%(version)s')
@click.option('--serverurl', help='The Plex server URL.',)
@click.option('--token', help='The Plex authentication token / X-Plex-Token.',)
@click.option('--library', help='The Plex library name.',)
@click.option('--assets', help='Which assets should be exported?', type=click.Choice(['all', 'posters', 'backgrounds', 'banners', 'themes']), required=True)
@click.option('--overlays', help='Export posters with overlay from Plex Meta Manager?', is_flag=True)
@click.option('--overwrite', help='Overwrite existing assets?', is_flag=True)
@click.option('--verbose', help='Show extra information?', is_flag=True)
@click.pass_context
def main(ctx, serverurl: str, token: str, library: str, assets: str, overwrite: bool, overlays: bool, verbose: bool):
    plex = Plex(serverurl, token, library, overwrite, overlays, verbose)

    if verbose:
        print('\033[94mASSETS:\033[0m', assets)
        print('\033[94mOVERWRITE:\033[0m', str(overwrite))
        print('\033[94mINCLUDE OVERLAYED POSTERS:\033[0m', str(overlays))
        print('\nGetting library items...')

    items = plex.getLibraryItems()

    print('\n' + str(len(items)) + ' items found.')

    if input("Start exporting assets? [y]/[n]: ") == 'y':
        for item in items:
            if verbose:
                print('\n\033[94mITEM:\033[0m', item.title)

            path = plex.getPath(item)
            if path == None:
                print('\033[91mERROR:\033[0m', 'failed to extract the path.')
                sys.exit()

            if (assets == 'all' or assets == 'posters') and hasattr(item, 'thumb') and item.thumb != None:
                plex.download(item.thumb, 'poster.jpg', path)
            if (assets == 'all' or assets == 'backgrounds') and hasattr(item, 'art') and item.art != None:
                plex.download(item.art, 'background.jpg', path)
            if (assets == 'all' or assets == 'banners') and hasattr(item, 'banner') and item.banner != None:
                plex.download(item.banner, 'banner.jpg', path)
            if (assets == 'all' or assets == 'themes') and hasattr(item, 'theme') and item.theme != None:
                plex.download(item.theme, 'theme.mp3', path)

            if plex.library.type == 'show':
                for season in item.seasons():
                    path = plex.getPath(season, True)
                    if path == None:
                        print('\033[91mERROR:\033[0m', 'failed to extract the path.')
                        sys.exit()

                    if (assets == 'all' or assets == 'posters') and hasattr(season, 'thumb') and season.thumb != None and season.title != None:
                        plex.download(season.thumb, (season.title if season.title != 'Specials' else 'season-specials-poster')+'.jpg', path)

        if verbose:
            print('\n\033[94mTOTAL SKIPPED:\033[0m', str(plex.skipped))
            print('\033[94mTOTAL DOWNLOADED:\033[0m', str(plex.downloaded))

    else:
         print('\nCancelled')
# run
if __name__ == '__main__':
    main(obj={})