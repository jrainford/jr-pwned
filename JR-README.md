# pwned-search with debugging JR

* `docker build -t jr-pwned .` Builds docker image
* `docker run -v$PWD/app:/app --rm jr-pwned [password]` Runs the pwned command pre-installed in a docker container

Debugging
* `docker run -it -v$PWD/app:/app -p 5678:5678  --entrypoint /bin/bash jr-pwned`
  * `python pwned.py [password]`
  * `python -m debugpy --listen 0.0.0.0:5678 --wait-for-client jr-pwned.py [passwd]`

.vscode/jr-keybinding.json is softlinked for convenience and hoping that it will be backed up

hello
