                    def ver = readFile 'VERSION'
                    ver = ver.replaceAll('\\n', '')
                    ver = ver.replaceAll('\\r', '')
                    echo "Version to tag: ${ver}"

                    def repo_url = "https://$BB_AUTH_PUSH_USR:$BB_AUTH_PUSH_PSW@$REPO_BASE/$REPO_PATH"

                    sh """#!/bin/bash
                    set -e

                    source /opt/miniconda3/etc/profile.d/conda.sh
                    conda activate pkg

                    git config --global user.name \"Jenkins\"
                    git config --global user.email \"jenkins_srvc@elsys.gtri.org\"

                    git clean -fxd
                    git reset --hard
                    git tag -a -m "Release ${ver}" v${ver}
                    git push $repo_url v${ver}
                    git checkout -b develop --track origin/develop
                    git merge origin/master --no-ff
                    python ./.ci/versionbump.py ./VERSION -i
                    git add VERSION
                    git commit -m "[jenkins][ci skip] Version Bump"
                    git push $repo_url develop
                    """