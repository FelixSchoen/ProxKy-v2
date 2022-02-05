from time import sleep
from typing import Type

from win32com import client

from src.main.configuration.config import CONFIG_INDESIGN_ID
from src.main.configuration.variables import Paths, Fonts


class InDesignHandler:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(InDesignHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        super().__init__()
        self.app = None
        self.study_document = None

    def __del__(self):
        if self.study_document is not None:
            self.study_document.Close(Saving=1852776480)
            pass

    def _get_study_document(self):
        if self.app is None:
            self.app = client.Dispatch(CONFIG_INDESIGN_ID)
        if self.study_document is None:
            self.study_document = self.app.Open(Paths.TEMPLATES + "/Study.idml")
        return self.study_document

    def get_text_lines(self, data: [([dict], dict)]) -> int:
        document = self._get_study_document()
        text_frame = next(x for x in document.TextFrames if x.Name == "Textbox")
        text_frame.Contents = ""

        for paragraph in data:
            if len(text_frame.Contents) > 0 and text_frame.Contents[-1] == "\n":
                text_frame.Contents = text_frame.Contents[:-1] + "\r"

            for character_dict in paragraph[0]:
                insertion_point = text_frame.InsertionPoints.LastItem()
                # Standards
                insertion_point.AppliedFont = Fonts.ORACLE_REGULAR["font"]
                insertion_point.PointSize = Fonts.ORACLE_REGULAR["size"]
                insertion_point.FontStyle = Fonts.ORACLE_REGULAR["style"]

                if "leading" in character_dict:
                    pass
                if "font" in character_dict:
                    insertion_point.AppliedFont = character_dict["font"]
                if "style" in character_dict and character_dict.get("style").lower() != "regular":
                    insertion_point.FontStyle = character_dict["style"]
                if "size" in character_dict:
                    insertion_point.PointSize = character_dict["size"]
                if "content" in character_dict:
                    content = character_dict.get("content")
                    insertion_point.Contents = content

            paragraph_dict = paragraph[1] if paragraph[1] is not None else dict()
            current_paragraph = text_frame.Paragraphs[text_frame.Paragraphs.Count - 1]
            # Standards
            current_paragraph.Justification = 1818584692
            current_paragraph.SameParaStyleSpacing = 1768386162
            current_paragraph.SpaceBefore = 0

            if "justification" in paragraph_dict:
                justification = paragraph_dict["justification"]
                value = 1818584692
                if justification == "CenterAlign":
                    value = 1667591796
                if justification == "LeftAlign":
                    value = 1818584692
                if justification == "RightAlign":
                    value = 1919379572
                current_paragraph.Justification = value
            if "space_before" in paragraph_dict:
                print("test")
                current_paragraph.SpaceBefore = paragraph_dict["space_before"] + "pt"
            if "spacing" in paragraph_dict:
                current_paragraph.SameParaStyleSpacing = paragraph_dict["spacing"] + "pt"

        return text_frame.Lines.Count
