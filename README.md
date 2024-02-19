# FastNotePad Export Parser
Allows a person to parse the export files of fastnotepad parser and populate a sqlite database with the results.

App link found here.

https://play.google.com/store/apps/details?id=net.fast_notepad_notes_app.fastnotepad&hl=en_US&gl=US

Fastnotepad organizes its backup files into two major sections:

1.  An index and preview section which includes a text preview, contentlength, and epoch time indicating LAST EDIT TIME, etc and a unique key field.
2.  A content section which links content to that key and has a few other fields for its use. Contains the value of the note field.

At the beginning of the field there is a fileid which uniquely identifies the file.

In between the two major sections is basically a searchable marker that contains numerous punctation marks.

The overall format of the file is very poor, but it is readable.

The fastNoteTool.py script has three events that fire while reading,  initially they will default to the 'print' statement and dump their content into stdout.

Implement these event handlers to capture the data as its being read.

  1. OnIRecord: Returns the index record with the creation time etc.
  2. OnCRecord: Returns the content record with the note, etc
  3. OnFileId: Returns the fileid of the export batch 

