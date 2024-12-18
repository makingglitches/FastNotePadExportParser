from .sql_result import SqlResult

from .NoteContents import Notecontents
from .Classification import Classification
from .ClassLookup import Classlookup
from .NoteContents_Updates import Notecontents_updates
from .Statistics import Statistics
from .HashTagsLookup import Hashtagslookup
from .HastTagNoteUpdates import Hasttagnoteupdates
from .NoteIndexes_Updates import Noteindexes_updates
from .UnifiedContent import Unifiedcontent
from .UnifiedContentUpdates import Unifiedcontentupdates
from .Files import Files
from .NoteIndexes import Noteindexes
from .HashTagNotes import Hashtagnotes


class DatabaseBinder:
    notecontents = Notecontents()
    classification = Classification()
    classlookup = Classlookup()
    notecontents_updates = Notecontents_updates()
    statistics = Statistics()
    hashtagslookup = Hashtagslookup()
    hasttagnoteupdates = Hasttagnoteupdates()
    noteindexes_updates = Noteindexes_updates()
    unifiedcontent = Unifiedcontent()
    unifiedcontentupdates = Unifiedcontentupdates()
    files = Files()
    noteindexes = Noteindexes()
    hashtagnotes = Hashtagnotes()
