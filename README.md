## Small Flask webapp for the LAN

#### Pull requests welcome :)

Run with `pipenv install` then `pipenv run python -m app`

- Reads server info using node-gamedig (via bash) and exposes it via the socket.io message `server_info`
- Allows to publish messages, that are exposed via the socket.io messages `messages` and `message-notify`
- Messages can be published to `/status/post` and cleared by POSTing to `/status/clear` 
- Serves webapp that uses this API to show information

The Frontend is mostly okay, but could use refactoring. Backend works, but is messy and is still missing features.

#### Desktop
![Desktop View](https://i.jaffa.pw/qemkRB7.png)

#### Mobile

![Mobile View](https://i.jaffa.pw/2GOIOYo.png)

