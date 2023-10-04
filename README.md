## Python API for the [AT Protocol](https://github.com/bluesky-social/atproto) (Authenticated Transfer Protocol) from BlueSky

This is my try to create API Bindings for the AT Protocol. It is written in Python and uses the requests library to send requests to the AT Protocol Server.

This is still a work in progress and probably not ready for production use as BlueSky stated that the AT Protocol is still in development and may change some stuff.

I currently only implemented the following functions:

``` Python 3.11
server = api.Server("example.com", "admin", "password")

server.createAccount("See API file for parameters")
# -> Creates Account. Needs an Invite Code
server.createInviteCode("See API file for parameters")
# -> Creates Invite Code
server.createInviteCodes("See API file for parameters")
# -> Creates multiple Invite Codes

admin = api.Admin("example.com", "admin", "password")

admin.getModerationReport("See API file for parameters")
# -> Gets a single Moderation Report
admin.getModerationReports("See API file for parameters")
# -> Gets multiple Moderation Reports

identity = api.Identity("example.com")

identity.resolveHandle("See API file for parameters")
# -> Resolves a Handle into an DID

```
