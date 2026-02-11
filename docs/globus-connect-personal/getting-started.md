# Globus Connect Personal

You can use Globus Connect Personal to quickly connect storage to Globus without having to go to all the trouble of setting up a Globus Connect Server endpoint. Use this when setting up a full Globus Connect Server endpoint is not worth the effort, or when only a small group of users will need to access the storage.

[Download Globus Connect Personal](https://www.globus.org/globus-connect-personal)

[Globus Connect Personal Documentation](https://docs.globus.org/globus-connect-personal/)

- University-managed Mac: Download from Self-Service app on your mac.

## Download Globus Connect Server

```
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
tar zxf globusconnectpersonal-latest.tgz
cd ./globusconnectpersonal-version
./globusconnectpersonal -setup
```

## Authentication
This globus user will own the collection. They can make other people administrator of the collection after it's created via the Globus Web app (https://app.globus.org)

## Name the endpoint
Give it a memorable name, will use the name to find the collection in the Globus web app.

## Run Globus Connect Personal

```
./globusconnectpersonal -start -restrict-paths rw~/ -shared-paths rw~/
```

- restrict-paths are the paths that users are able to browse in the Globus web app
- shared-paths are the paths that are allowed to be shared with other users via guest collections

Notes:

- Globus connect personal runs as the local user on the server that ran the globusconnectpersonal command.
- Good to run this command as a local account on the server that isn't tied to any one particular person.

## Make Globus Connect personal endpoint a subscribed endpoint

- open https://app.globus.org
- Select Collections
- Search for the Globus Connect Personal Mapped collection 
- Select Edit Subscription Status
- Add it to the University of Sydney subscription
- If you can't see the University of Sydney subscription, ask to be added to the University of Sydney Globus subscription Group

Reference: [Globus FAQs](https://docs.globus.org/faq/subscriptions/#subscribing_a_globus_connect_personal_collection)


## Create a "guest collection" on the Globus Connect Personal mapped collection

Need to create a guest collection to share a globus connect personal collection with others. Normally guest collections are only available to the user who created the Globus Connect Personal connection

- Find the globus-connect-personal collection in the Globus web portal
- Click the collections tab
- Create guest collection
- After creation, add permissions to share the guest collection with those that need access


