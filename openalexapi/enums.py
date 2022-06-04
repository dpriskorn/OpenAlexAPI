"""
Copyright 2022 Dennis Priskorn
"""
from enum import Enum

# Pulled from https://api.crossref.org/types
class WorkType(Enum):
    BOOK = "book"
    BOOK_CHAPTER = "book-chapter"
    BOOK_PART = "book-part"
    BOOK_SECTION = "book-section"
    BOOK_SERIES = "book-series"
    BOOK_SET = "book-set"
    BOOK_TRACK = "book-track"
    COMPONENT = "component"
    DATASET = "dataset"
    DISSERTATION = "dissertation"
    EDITED_BOOK = "edited-book"
    GRANT = "grant"
    JOURNAL = "journal"
    JOURNAL_ARTICLE = "journal-article"
    JOURNAL_ISSUE = "journal-issue"
    JOURNAL_VOLUME = "journal-volume"
    MONOGRAPH = "monograph"
    OTHER = "other"
    PEER_REVIEW = "peer-review"
    POSTED_CONTENT = "posted-content"
    PROCEEDINGS = "proceedings"
    PROCEEDINGS_ARTICLE = "proceedings-article"
    PROCEEDINGS_SERIES = "proceedings-series"
    REFERENCE_BOOK = "reference-book"
    REFERENCE_ENTRY = "reference-entry"
    REPORT = "report"
    REPORT_SERIES = "report-series"
    STANDARD = "standard"
    STANDARD_SERIES = "standard-series"

#used in host_venue
class VersionType(Enum):
    PUBLISHED_VERSION="publishedVersion"
    ACCEPTED_VERSION="acceptedVersion"
    SUBMITTED_VERSION="submittedVersion"

#used in institituion
class InstitutionalRelationship(Enum):
    PARENT="parent"
    CHILD="child"
    RELATED="related"
    
#used in institituion
class InstitutionType(Enum):
    EDUCATION="education"
    HEALTHCARE="healthcare"
    COMPANY="company"
    ARCHIVE="archive"
    NONPROFIT="nonprofit"
    GOVERNMENT="government"
    FACILITY="facility"
    OTHER="other"
    
#used in openaccess
class OpenAccessStatus(Enum):
    GOLD="gold"
    GREEN="green"
    HYBRID="hybrid"
    BRONZE="bronze"
    CLOUD="cloud"