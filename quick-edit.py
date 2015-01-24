from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec
import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.edam.error.ttypes import EDAMUserException
import os
import sys
from urlparse import urlparse, parse_qsl

def localnotebooks(notebooks, authToken, noteStore):
	notebooks_name=list()
	notebooks_guid=list()

	for counter, notebook in enumerate(notebooks):
		print str(counter) + ':' + str(notebook.name)
		notebooks_name.append(notebook.name)
		notebooks_guid.append(notebook.guid)
	try:
		notebook_selection=raw_input("select notebook number to edit:")
		notebook_selection=int(notebook_selection)
	except:
		localnotebooks(notebooks)


	notebook_filter=NoteStoreTypes.NoteFilter()
	notebook_filter.notebookGuid=notebooks_guid[notebook_selection]
	result_spec = NotesMetadataResultSpec(includeTitle=True)
	note_results=noteStore.findNotesMetadata(authToken, notebook_filter,0 , 40000, result_spec)

	note_titles=list()
	note_guids=list()
	for counter, note in enumerate(note_results.notes):
		print str(counter) +":"+str(note.title)
		note_titles.append(note.title)
		note_guids.append(note.guid)

	try:
		note_selection=raw_input("select note number to edit:")
		note_selection=int(note_selection)
	except:
		localnotebooks(notebooks)

	#get note enml
	note=noteStore.getNote(authToken, note_guids[note_selection], True, False, False, False)

	#save enml to file
	f = open(note_titles[note_selection]+".enml", 'w')
	f.write(note.content)
	f.close()

	while True:
		print "enml saved at . . . \n\n%s\n\n Please edit the file and return here when you are done.\n" % (os.getcwd() + "/" + note_titles[note_selection] +'.enml')
		done=raw_input("are you done?  y/n: ")

		if done == 'y':
			print "uploading edit to evernote . . . "
			break
		if done == 'n':
			print "ok well that was useless\n\n"
		else:
			print "invalid response\n\n"


	f = open(note_titles[note_selection]+".enml", 'r')
	enml=f.read()
	note.content=enml
	noteStore.updateNote(authToken, note)
	print "DONE"
	try:
		selection=raw_input("Select . . . \n(1) to edit another note witht the same auth\n(2) to start over with new auth\n(3) to quit\n enter a number: ")
		selection=str(selection)

		if selection =='1':
			localnotebooks(notebooks, authToken, noteStore)
		elif selection == '2':
			main()
		elif selection == '3':
			print "exiting . . ."
			sys.exit			
		else:
			print "invalid input. Starting over . . .\n"
			main()
	except:
		main()


def linkednotebooks(notebooks, authToken, noteStore, client):
	notebooks_name=list()
	notebooks_guid=list()

	for counter, notebook in enumerate(notebooks):
		print str(counter) + ':' + str(notebook.shareName)
		notebooks_name.append(notebook.shareName)
		notebooks_guid.append(notebook.guid)

	try:
		notebook_selection=raw_input("select notebook number to edit:")
		notebook_selection=int(notebook_selection)
	except:
		linkednotebooks(notebooks)	

	
	linked_notebook=notebooks[notebook_selection]

	#get sharedNoteSTore 
	sharedNoteStore=client.get_shared_note_store(linked_notebook)

	#get GUID of notebook
	guid=sharedNoteStore.listNotebooks()[0].guid

	#filter notes for only in notebook selected
	notebook_filter=NoteStoreTypes.NoteFilter()
	notebook_filter.notebookGuid=guid
	result_spec = NotesMetadataResultSpec(includeTitle=True)
	note_results=sharedNoteStore.findNotesMetadata(sharedNoteStore.token, notebook_filter,0 , 40000, result_spec)

	note_titles=list()
	note_guids=list()
	for counter, note in enumerate(note_results.notes):
		print str(counter) +":"+str(note.title)
		note_titles.append(note.title)
		note_guids.append(note.guid)

	try:
		note_selection=raw_input("select note number to edit:")
		note_selection=int(note_selection)
	except:
		linkednotebooks(notebooks)

	#get note enml
	note=sharedNoteStore.getNote(sharedNoteStore.token, note_guids[note_selection], True, False, False, False)

	#save enml to file
	f = open(note_titles[note_selection]+".enml", 'w')
	f.write(note.content)
	f.close()

	while True:
		print "enml saved at . . . \n\n%s\n\n Please edit the file and return here when you are done.\n" % (os.getcwd()  + "/" + note_titles[note_selection] +'.enml')
		done=raw_input("are you done?  y/n: ")

		if done == 'y':
			print "uploading edit to evernote . . . "
			break
		if done == 'n':
			print "ok well that was useless\n\n"
		else:
			print "invalid response\n\n"


	f = open(note_titles[note_selection]+".enml", 'r')
	enml=f.read()
	note.content=enml
	try:
		sharedNoteStore.updateNote(sharedNoteStore.token, note)
	except EDAMUserException:
		print "FAILURE: do you have authority to edit this note?"
	print "DONE"

	try:
		selection=raw_input("Select . . . \n(1) to edit another note witht the same auth\n(2) to start over with new auth\n(3) to quit\n enter a number: ")
		selection=str(selection)

		if selection =='1':
			linkednotebooks(notebooks, authToken, noteStore, client)
		elif selection == '2':
			main()
		elif selection == '3':
			print "exiting . . ."
			sys.exit			
		else:
			print "invalid input. Starting over . . .\n"
			main()
	except:
		main()	



def main():
	print "This program selects notes and then donwloads the ENML for you to edit.\nAfter editing you can then update the note via this tool as well\n"
	
	try:
		selection=raw_input("Select (1) for sandbox or (2) for production:")
		selection=str(selection)

		if selection =='1':
			EN_URL="https://www.evernote.com"
			sandbox = True
		elif selection == '2':
			EN_URL = "https://sandbox.evernote.com"
			sandbox=False
		else:
			print "invalid input\n"
			main()
	except:
		main()	

	try:
		selection=raw_input("Select (1) for dev token or (2) for OAuth:")
		selection=str(selection)

		if selection =='1':

			try:
				authToken=raw_input("developer token:")
				client = EvernoteClient(token=authToken, sandbox=sandbox)

				userStore = client.get_user_store()
				noteStore = client.get_note_store()
			except EDAMUserException:
				print "invalid token"
				main()

		elif selection == '2':
			try:
				CONSUMER_KEY = raw_input("Please enter your consumer key: ")
				CONSUMER_SECRET = raw_input("Please enter your consumer secret: ")

				client = EvernoteClient(
								consumer_key=CONSUMER_KEY,
								consumer_secret=CONSUMER_SECRET,
								sandbox= sandbox
								)

				request_token = client.get_request_token("http://localhost")
				oauth_token = request_token['oauth_token'] 
				oauth_token_secret = request_token['oauth_token_secret']
				authorize_url = client.get_authorize_url(request_token)

				AUTH_URL = raw_input("Please go to:\n"+authorize_url+"\nand authorize the application and paste the resulting URL here: ")

				query= urlparse(AUTH_URL).query
				params=parse_qsl(query)
				params=dict(params)

				authToken = client.get_access_token(request_token['oauth_token'], request_token['oauth_token_secret'], params['oauth_verifier'])

				userStore = client.get_user_store()
				noteStore = client.get_note_store()
			except EDAMUserException:
				print "OAuth Error"
				main()
			
		else:
			print "invalid input\n"
			main()
	except EDAMUserException:
		main()


	selection=raw_input("Select (1) for user's notebooks or (2) for linked notebooks:")
	if selection == '1':
		notebooks=noteStore.listNotebooks()
		localnotebooks(notebooks, authToken, noteStore)
	elif selection =='2':
		print "warning: please make sure you have edit access to the notebook\nbefore you attempt to edit the note"
		selection=raw_input("are you sure you want to continue? y/n:")
		if selection == 'y':
			notebooks=noteStore.listLinkedNotebooks()
			linkednotebooks(notebooks, authToken, noteStore, client)
		else:
			print "returning to main menu . . . \n"
			main()
	else:
		print "invalid selection try again\n\n"
		main()

if __name__ =="__main__":
	main()
