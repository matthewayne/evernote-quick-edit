# Evernote Tools
A selection of tools that aid in the development of applications with an Evernote integration.

### Generate Access Token
A command line tool that generates a access token from a OAuth key and secret.

dependencies: evernote (install via "pip install evernote")

Usage:
```bash
$ python generate_access_token.py
Please enter your consumer key: [insert API key here]
Please enter your consumer secret: [insert API secret here]
Please go to:
https://www.evernote.com/OAuth.action?oauth_token=apikey.14B195A.68747370FA2A2F6C6F63616C686F7374.865B60E2A99D2BB650CEC75448ED330D
and authorize the application and paste the resulting URL here: http://localhost/?oauth_token=newkey.14B195E825A.687474703A2F2F6C6F63616C686F7374.865B60E2A99D2BB650CEC75448ED330D&oauth_verifier=7989D3B877358338CF417ECB7CBCDA0529&sandbox_lnb=false

Here is your auth token:

S=s432:U=489be66:E=152710fe5c9:C=14b195eb888:P=185:A=newkey:V=2:B=1203276a-214e-4164-197a-113b082fd17f:H=934418f99d2d293f7e05637b4d621510


$
```

If you don't have an Evernote API key go to https://dev.evernote.com/#apikey

### Evernote Quick Edit
A command line tool that edits the ENML contents of a Evernote note.

dependencies: evernote (install via "pip install evernote")

usage:
```
$ python quick-edit.py
This program selects notes and then donwloads the ENML for you to edit.
After editing you can then update the note via this tool as well

Select (1) for sandbox or (2) for production:1
Select (1) for dev token or (2) for OAuth:1
developer token:S=s1:U=8fa39:E=1516a178f19:C=15b136662a0:P=1cd:A=en-devtoken:V=2:H=4db60901ef59fc1dea800f97c7cb798d
Select (1) for user's notebooks or (2) for linked notebooks:1
0:Giphy
1:newkey
2:THE Notebook
3:TestApp
select notebook number to edit:3
0:This is a test note!
1:Hello Developer Forums!!!
2:How are you doin'?
select note number to edit:0
enml saved at . . .

/path/to/current/directory/This is a test note!.enml

 Please edit the file and return here when you are done.

are you done?  y/n: y
uploading edit to evernote . . .
DONE
Select . . .
(1) to edit another note witht the same auth
(2) to start over with new auth
(3) to quit
 enter a number: 3
exiting . . .
$
```
