from enum import Enum



class BlogStatus(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    EDITED = "EDITED"
    PUBLISHED = "PUBLISHED"