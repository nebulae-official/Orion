from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, validator

# --- User Objects ---
# Ref: https://developers.notion.com/reference/user-object


class PartialUser(BaseModel):
    """Represents a partial User object, often returned in created_by/last_edited_by."""

    object: Literal["user"] = "user"
    id: str


class User(PartialUser):
    """Represents a full User object."""

    type: Literal["person", "bot"] | None = None
    name: str | None = None
    avatar_url: HttpUrl | str | None = (
        None  # Allow string for potential data URLs? Pydantic handles HttpUrl validation
    )
    person: dict[str, str] | None = None  # Only present for type="person"
    bot: dict[str, Any] | None = None  # Only present for type="bot"

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )


# --- Rich Text Objects ---
# Ref: https://developers.notion.com/reference/rich-text-object


class Annotations(BaseModel):
    """Represents annotations applied to rich text."""

    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: str = "default"  # Can be enum later if needed

    model_config = ConfigDict(extra="ignore")


class RichTextBase(BaseModel):
    """Base for different Rich Text types."""

    plain_text: str
    href: HttpUrl | str | None = None  # Allow string for relative links?
    annotations: Annotations

    model_config = ConfigDict(extra="ignore")


class TextData(BaseModel):
    """Text content within a RichText object."""

    content: str
    link: dict[str, str] | None = None  # Link object structure


class RichTextText(RichTextBase):
    """Rich text object of type 'text'."""

    type: Literal["text"] = "text"
    text: TextData


class IconData(BaseModel):
    """Icon data for callout and other blocks."""

    type: Literal["emoji", "external"]  # Can be enum later
    emoji: str | None = None  # Only for type="emoji"
    external: dict[str, str] | None = None  # Only for type="external"


class MentionData(BaseModel):
    """Base for different mention types."""

    # Contains type-specific fields like 'user', 'page', 'database', 'date', 'link_preview'
    # Using Dict[str, Any] for now, can be more specific later


class UserMentionData(MentionData):
    """Mention data for user type."""

    user: User | PartialUser


class PageMentionData(MentionData):
    """Mention data for page type."""

    page: dict[str, str]  # {"id": "uuid"}


class DatabaseMentionData(MentionData):
    """Mention data for database type."""

    database: dict[str, str]  # {"id": "uuid"}


class DateMentionData(MentionData):
    """Mention data for date type."""

    date: dict[str, Any]  # Date object structure


class LinkPreviewMentionData(MentionData):
    """Mention data for link_preview type."""

    link_preview: dict[str, str]  # {"url": "http://..."}


class TemplateMentionDateData(MentionData):
    """Mention data for template_mention_date type."""

    template_mention_date: str  # e.g., "today", "now"


class TemplateMentionUserData(MentionData):
    """Mention data for template_mention_user type."""

    template_mention_user: str  # e.g., "me"


# Add other template mention types if needed


class RichTextMention(RichTextBase):
    """Rich text object of type 'mention'."""

    type: Literal["mention"] = "mention"
    # The 'mention' field's structure depends on the mention type within it
    mention: dict[str, Any]  # Needs further parsing based on mention['type']


class EquationData(BaseModel):
    """Equation content within a RichText object."""

    expression: str  # LaTeX expression


class RichTextEquation(RichTextBase):
    """Rich text object of type 'equation'."""

    type: Literal["equation"] = "equation"
    equation: EquationData


# --- Union Type for Rich Text ---
# This allows Pydantic to parse into the correct RichText subclass based on 'type'
AnyRichText = RichTextText | RichTextMention | RichTextEquation

# --- File Objects ---
# Ref: https://developers.notion.com/reference/file-object


class FileDataBase(BaseModel):
    """Base for file data types."""

    url: HttpUrl | str
    expiry_time: datetime | None = None  # Only for type="file"


class FileDataExternal(FileDataBase):
    """File data for type 'external'."""

    # Only has 'url' from base


class FileDataFile(FileDataBase):
    """File data for type 'file' (Notion-hosted)."""

    # Has 'url' and 'expiry_time' from base


class FileObject(BaseModel):
    """Represents a Notion File object."""

    type: Literal["external", "file"]
    caption: list[AnyRichText] = Field(default_factory=list)
    name: str | None = None  # Name might be present for display
    # Use discriminated union for file data based on 'type'
    external: FileDataExternal | None = None
    file: FileDataFile | None = None

    model_config = ConfigDict(extra="ignore")

    @validator("file", always=True)
    def check_file_data(cls, file_data, values):
        if values.get("type") == "file" and file_data is None:
            raise ValueError("Missing 'file' data for file type 'file'")
        if values.get("type") == "external" and file_data is not None:
            raise ValueError("Unexpected 'file' data for file type 'external'")
        return file_data

    @validator("external", always=True)
    def check_external_data(cls, external_data, values):
        if values.get("type") == "external" and external_data is None:
            raise ValueError("Missing 'external' data for file type 'external'")
        if values.get("type") == "file" and external_data is not None:
            raise ValueError("Unexpected 'external' data for file type 'file'")
        return external_data


# --- Other Common Objects ---


class SelectOption(BaseModel):
    """Represents an option in a Select or Multi-select property."""

    id: str
    name: str
    color: str = "default"  # Can be enum later

    model_config = ConfigDict(extra="ignore")


# Add more common objects like Parent types, Date ranges etc. as needed.
