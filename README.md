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
6. Create superuser: `python manage.py createsuperuser`
7. Go to `localhost:8000/admin`, go to "Social Applications", and add the application with the "Client ID" and "Secret Key" that we got from our GCP console.