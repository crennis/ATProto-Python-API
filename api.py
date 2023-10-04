import requests
import base64
import json


class Server:
    def __init__(self, server: str, username: str, password: str):
        """ Create a Server-instance of the ATProto API. Requires Admin access
        :param server: The server ATProto is running on
        :type server: str
        :param username: the username to authenticate with
        :type username: str
        :param password: the password to authenticate with
        :type password: str
        """
        self.server = server
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Basic " + base64.b64encode((username + ":" + password).encode("utf-8")).decode("utf-8"),
        }

        self.endpoints = {
            "createAccount": f"https://{self.server}/xrpc/com.atproto.server.createAccount",
            "createInviteCode": f"https://{self.server}/xrpc/com.atproto.server.createInviteCode",
            "createInviteCodes": f"https://{self.server}/xrpc/com.atproto.server.createInviteCodes",
        }

    def createAccount(self, email: str, handle: str, password: str,
                      did: str= None, inviteCode: str = None, recoveryKey: str = None):
        """ Create a new account
        :param email: The email of the account
        :type email: str
        :param handle: The handle of the account (handle/username.atprotoserver.example)
        :type handle: str
        :param did: The DID of the account (optional)
        :type did: str
        :param inviteCode: The invite code to use (optional)
        :type inviteCode: str
        :param password: The password of the account
        :type password: str
        :param recoveryKey: The recovery key of the account (optional)
        :type recoveryKey: str
        :return:
        """
        data = {"email": email,
                "handle": handle,
                "password": password,
                **({"did": did} if did is not None else {}),
                **({"inviteCode": inviteCode} if inviteCode is not None else {}),
                **({"recoveryKey": recoveryKey} if recoveryKey is not None else {})
                }
        req = requests.post(self.endpoints["createAccount"], headers=self.headers, data=json.dumps(data))
        return req.json()

    def createInviteCode(self, useCount: int, forAccount: str = None):
        """ Create a single invite code
        :param useCount: How many times the invite code can be used
        :type useCount: int
        :param forAccount: The account the invite code is for (optional)
        :type forAccount: str: account DID
        :return: json-response with the generated invite code
        """

        data = {"useCount": useCount,
                **({"forAccount": forAccount} if forAccount is not None else {})
                }
        req = requests.post(self.endpoints["createInviteCode"], headers=self.headers, data=json.dumps(data))
        return req.json()

    def createInviteCodes(self, codeCount: int = 1, useCount: int = 1, forAccounts: list = None):
        """ Create multiple invite codes
        :param codeCount: How many invite codes to create
        :type codeCount: int
        :param useCount: How many times the invite code can be used
        :type useCount: int
        :param forAccounts: The accounts the invite codes are for (optional)
        :type forAccounts: list: account DIDs
        :return: json-response with the generated invite codes
        """

        data = {"codeCount": codeCount or 1,
                "useCount": useCount,
                **({"forAccounts": forAccounts} if forAccounts is not None else {})
                }

        req = requests.post(self.endpoints["createInviteCodes"], headers=self.headers, data=json.dumps(data))
        return req.json()

class Admin:
    def __init__(self, server: str, username: str, password: str):
        """ Create a Admin-instance of the ATProto API. Requires Admin access
        :param server: The server ATProto is running on
        :type server: str
        :param username: the username to authenticate with
        :type username: str
        :param password: the password to authenticate with
        :type password: str
        """
        self.server = server
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Basic " + base64.b64encode((username + ":" + password).encode("utf-8")).decode(
                "utf-8"),
        }

        self.endpoints = {
            "getModerationReports": f"https://{self.server}/xrpc/com.atproto.admin.getModerationReports",
            "getModerationReport": f"https://{self.server}/xrpc/com.atproto.admin.getModerationReport",
        }
        self.actiontypes = {
            "takedown": "com.atproto.admin.defs#takedown",
            "flag": "com.atproto.admin.defs#flag",
            "acknowledge": "com.atproto.admin.defs#acknowledge",
            "escalate": "com.atproto.admin.defs#escalate",
        }

    def getModerationReport(self, id: int):
        data = {"id": id}
        req = requests.get(f'{self.endpoints["getModerationReport"]}?id={id}', headers=self.headers)
        return req.json()

    def getModerationReports(self, subject: str = "", ignoreSubjects: list = None, actionedBy: str = "",
                             reporters: list = None, resolved: bool = None, actionType: str = "", limit: int = 50,
                             cursor: str = "", reverse: bool = False):
        """ Get moderation reports
        :param subject: The subject of the report (optional)
        :type subject: str
        :param ignoreSubjects: Subjects to ignore (optional)
        :type ignoreSubjects: list: str
        :param actionedBy: The account that actioned the report (optional)
        :type actionedBy: str | list: account DID(-s)
        :param reporters: The accounts that reported the subject (optional)
        :type reporters: list: account DIDs
        :param resolved: Whether the report is resolved (optional)
        :type resolved: bool
        :param actionType: The action type of the report (optional)
        :type actionType: str: action type (see self.actiontypes)
        :param limit: How many reports to get (Min: 1, Max: 100, Default: 50)
        :type limit: int
        :param cursor:
        :type cursor:
        :param reverse: Whether to reverse the results (optional)
        :type reverse: bool
        :return: json-response with the reports
        """

        mapping = {None: "", True: "true", False: "false"}

        if ignoreSubjects:
            ignoreSubjects = ",".join(ignoreSubjects)
        elif not ignoreSubjects:
            ignoreSubjects = ""

        if reporters:
            reporters = ",".join(reporters)
        elif not reporters:
            reporters = ""

        resolved = mapping.get(resolved)
        reverse = mapping.get(reverse)

        parameters = f"?subject={subject}&ignoreSubjects={ignoreSubjects}&actionedBy={actionedBy}&reporters={reporters}&resolved={resolved}&actionType={actionType}&limit={limit}&cursor={cursor}&reverse={reverse}"
        print(parameters)

        req = requests.get(f'{self.endpoints["getModerationReports"]}{parameters}', headers=self.headers)
        return req.json()

class Identity:
    def __init__(self, server: str):
        """ Create a Identity-instance of the ATProto API.
        :param server: The server ATProto is running on
        :type server: str
        """
        self.server = server
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        self.endpoints = {
            "getModerationReports": f"https://{self.server}/xrpc/com.atproto.identity.resolveHandle",
            "getModerationReport": f"https://{self.server}/xrpc/com.atproto.identity.updateHandle",
        }

    def resolveHandle(self, handle: str): # Doesn't Require Account
        """ Resolve a handle
        :param handle: The handle to resolve
        :type handle: str
        :return: json-response with the resolved handle
        """
        req = requests.get(f'{self.endpoints["getModerationReports"]}?handle={handle}', headers=self.headers)
        return req.json()
