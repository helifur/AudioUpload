# Audio Uploading Service

A service that represents audio management system with Yandex ID authorization


## Features

- Full Yandex ID support
- PostgreSQL and Redis to store data
- Alembic migrations to properly update roles


## Installation

Clone this repo

```bash
git clone https://github.com/helifur
```

*Before proceeding go to https://yandex.ru/dev/id/doc/ru/how-to and learn how to create Yandex application to integrate authorization*
## Environment Variables

To run this project, you will need to add some environment variables to your .env file.
Vars below can be found in your Yandex OAuth app dashboard.

`CLIENT_ID`: ClientID 

`CLIENT_SECRET`: Client secret

`REDIRECT_URI`: Redirect URI

The rest is up to you 😉
## Usage
After all steps above just start docker containers like this:

```bash
docker compose up --build
```

To open PGAdmin, go to `localhost:105`.

To try methods, go to `localhost:8000/docs`.
## Support

- *How to get secret_code that requires `auth` method?*

    You need to open this link in your browser:
    `https://oauth.yandex.ru/authorize?response_type=code&client_id=CLIENT_ID`, where `CLIENT_ID` is your `ClientID` in the Yandex OAuth dashboard.
    
    Remember that `secret_code` is **ONE-TIME USE**!!! In order to get a new one, just follow the link again.

## License

[MIT](https://choosealicense.com/licenses/mit/)

