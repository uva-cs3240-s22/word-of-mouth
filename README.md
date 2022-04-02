# Word Of Mouth


## How to start developing:
1. Create a [GCP App](https://console.cloud.google.com/home/)
2. Go to [API Overview](https://console.cloud.google.com/apis/)
3. Go to "Credentials" on the menu to the left
4. Hit Create Credentials at the top of the page
   1. For the "Approved JavaScript Origins", set it to be `http://localhost:8000`. (TODO: We need to add our heroku deployments to this list)
   2. For the "Authorized Redirect URLs", set it to be `http://localhost:8000/accounts/google/login/callback/`. (TODO: See above)
   3. (side note: if you are running into errors, keep in mind that `localhost` and `127.0.0.1` are two different domain names, even though they resolve to the same place)
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser` - note that if you create it with your google email that you'll be testing with, there will be a conflict, so feel free to use a dummy email here.
7. Copy `.env.template` over to your very own local `.env` file - note that this file is in `.gitignore` for a good reason - we don't want anybody to have access to anybody else's `.env` file.
8. Copy the client id and secret key (gotten from the GCP console) into the corresponding environment variables into your new `.env`.
 