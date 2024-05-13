# -TODO

# - Get release tag from halflife-unified-sdk hook

# - Download all the assets on it's release and repack within the source code of this repo

# - exclude:
#   .github/workflows/build.yml
#   README.md
#   LICENCE
#   HALFLIFE_SDK_LICENCE
#   .gitignore

# - Create a release with the same tag from hlu-sdk

# - Copy changelog.md from HLU-SDK within this release

# - Do a discord webhook pinging LP role with a embeed maybe


import requests, shutil, os

def dl(owner, repo, release_tag, token):
    headers = {'Authorization': f'token {token}'}
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info['assets']
        for asset in assets:
            if not release_tag in asset['name']:
                asset_url = asset['browser_download_url']
                asset_name = asset['name']
                with open(asset_name, 'wb') as f:
                    asset_response = requests.get(asset_url)
                    f.write(asset_response.content)

                if asset_name.startswith( 'client' ) or asset_name.startswith( 'libopenal' ) or asset_name.startswith( 'openal' ):
                    if not os.path.exists( 'cl_dlls' ):
                        os.mkdir( 'cl_dlls' )
                    shutil.move( asset_name, f'cl_dlls/{asset_name}' )

                elif asset_name.startswith( 'server' ):
                    if not os.path.exists( 'dlls' ):
                        os.mkdir( 'dlls' )
                    shutil.move( asset_name, f'dlls/{asset_name}' )
    else:
        print(f"{response.status_code}")

owner = 'Mikk155'
repo = 'halflife-unified-sdk'
release_tag = '0'
token = ""

dl(owner, repo, release_tag, token)
