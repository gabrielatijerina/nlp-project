"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "freeCodeCamp/freeCodeCamp",
    "vuejs/vue",
    "facebook/react",
    "tensorflow/tensorflow",
    "twbs/bootstrap",
    "donnemartin/system-design-primer",
    "ohmyzsh/ohmyzsh",
    "public-apis/public-apis",
    "microsoft/vscode",
    "torvalds/linux",
    "airbnb/javascript",
    "trekhleb/javascript-algorithms",
    "TheAlgorithms/Python",
    "d3/d3",
    "facebook/react-native",
    "ytdl-org/youtube-dl",
    "electron/electron",
    "axios/axios",
    "facebook/create-react-app",
    "nodejs/node",
    "kubernetes/kubernetes",
    "30-seconds/30-seconds-of-code",
    "microsoft/terminal",
    "tensorflow/models",
    "vercel/next.js",
    "iluwatar/java-design-patterns",
    "FortAwesome/Font-Awesome",
    "goldbergyoni/nodebestpractices",
    "laravel/laravel",
    "nvbn/thefuck",
    "atom/atom",
    "spring-projects/spring-boot",
    "elastic/elasticsearch",
    "jquery/jquery",
    "microsoft/PowerToys",
    "opencv/opencv",
    "typicode/json-server",
    "netdata/netdata",
    "keras-team/keras",
    "chrislgarry/Apollo-11",
    "httpie/httpie",
    "josephmisiti/awesome-machine-learning",
    "h5bp/html5-boilerplate",
    "lodash/lodash",
    "Semantic-Org/Semantic-UI",
    "h5bp/Front-end-Developer-Interview-Questions",
    "redis/redis",
    "yangshun/tech-interview-handbook",
    "chartjs/Chart.js",
    "socketio/socket.io",
    "bitcoin/bitcoin",
    "ionic-team/ionic-framework",
    "necolas/normalize.css",
    "ReactTraining/react-router",
    "huggingface/transformers",
    "scikit-learn/scikit-learn",
    "moment/moment",
    "psf/requests",
    "ReactiveX/RxJava",
    "impress/impress.js",
    "mermaid-js/mermaid",
    "Alamofire/Alamofire",
    "serverless/serverless",
    "prettier/prettier",
    "juliangarnier/anime",
    "godotengine/godot",
    "ColorlibHQ/AdminLTE",
    "apache/superset",
    "parcel-bundler/parcel",
    "square/retrofit",
    "spring-projects/spring-framework",
    "jekyll/jekyll",
    "home-assistant/core",
    "meteor/meteor",
    "jaywcjlove/awesome-mac",
    "grafana/grafana",
    "NARKOZ/hacker-scripts",
    "tailwindlabs/tailwindcss",
    "syncthing/syncthing",
    "strapi/strapi",
    "apache/dubbo",
    "deepfakes/faceswap",
    "iamkun/dayjs",
    "mozilla/pdf.js",
    "python/cpython",
    "vsouza/awesome-ios",
    "TryGhost/Ghost",
    "hexojs/hexo",
    "gulpjs/gulp",
    "alvarotrigo/fullPage.js",
    "Marak/faker.js",
    "fastlane/fastlane",
    "NationalSecurityAgency/ghidra",
    "beego/beego",
    "jashkenas/underscore",
    "skylot/jadx",
    "agalwood/Motrix",
    "pingcap/tidb",
    "bayandin/awesome-awesomeness",
    "microsoft/playwright",
    "go-gorm/gorm",
    "iview/iview",
    "cheeriojs/cheerio",
    "mobxjs/mobx",
    "GitbookIO/gitbook",
    "anuraghazra/github-readme-stats",
    "ryanoasis/nerd-fonts",
    "google-research/bert",
    "bumptech/glide",
    "airbnb/lottie-android",
    "immutable-js/immutable-js",
    "tiangolo/fastapi",
    "jondot/awesome-react-native",
    "Blankj/AndroidUtilCode",
    "FFmpeg/FFmpeg",
    "ctripcorp/apollo",
    "typescript-cheatsheets/react",
    "sherlock-project/sherlock",
    "gorhill/uBlock",
    "PowerShell/PowerShell"

]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)
