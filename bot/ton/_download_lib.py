import io
import zipfile
import requests

# https://github.com/settings/tokens?type=beta
# token must have REPO scope with ACTIONS: READ permission
# current token expires soon
ACCESS_TOKEN = "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"

artifact_list = requests.get("https://api.github.com/repos/ton-blockchain/ton/actions/artifacts").json()

for artifact in artifact_list["artifacts"]:
    name = artifact["name"]
    # find first linux x64 artifact
    if name.startswith("ton-ubuntu") and not name.endswith("arm64"):
        print("Found artifact:", artifact["name"], artifact["url"])
        download_url = artifact["archive_download_url"]
        break
else:
    raise RuntimeError("No artifacts found")

print("Downloading artifact:", download_url)
r = requests.get(download_url, headers={"Authorization": "token " + ACCESS_TOKEN})

print("Extracting libtonlibjson.so.0.5")

with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    z.extract("libtonlibjson.so.0.5", path=".")

print("Done!")
