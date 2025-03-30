# Audio Uploading Service

A service that represents audio management system with Yandex ID authorization


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
## Support

- *How to get secret_code that requires `auth` method?*

    You need to open this link in your browser:
    `https://oauth.yandex.ru/authorize?response_type=code&client_id=8d7e704d59674519b7d9a0e1c458b5d5`, where `client_id` is your `ClientID` in the Yandex OAuth dashboard.
    
    Remember that `secret_code` is **ONE-TIME USE**!!! In order to get a new one, just follow the link again.

## License

[MIT](https://choosealicense.com/licenses/mit/)

