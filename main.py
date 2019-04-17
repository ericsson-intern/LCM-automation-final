
from mavenbox.util import update_artifacts, url_build
import json
import sys
import os
import shutil

BASE = "gerrit.epk.ericsson.se"
LINKS = [
    'charging/com.ericsson.bss.rm.charging.bundle',
    'charging/com.ericsson.bss.rm.charging.dataaccess'
]

def update_interface(csv,review):

    for link in LINKS:
        url = url_build('ssh',29418,BASE,link)
        git = update_artifacts(CACHE='.cache',REPO_URL=url,ARTIFACTS_CSV=csv, COMMIT='CDAC to 8.47.0 -- ignore-commit')

        if not review.startswith('$'):
            git.set_reviewers(review)

        git.push()
        raw_input("Press Enter to continue...")
    pass





























# def update_interface(csv,reviewers):

#     with open('./repobox/git_links.json') as f:
#         links = json.loads(f.read())

#     for link in links[:3]:
#         url = url_build('ssh',29418,link['base'],link['repo'])

#         git = update_dependency(COLLECTION_ROOT=COLLECTION_ROOT, ARTIFACTS_CSV=csv,REPO_URL=url)
#         git.set_reviewers(reviewers)
#         git.push()
#         raw_input("Press Enter to continue...")



    