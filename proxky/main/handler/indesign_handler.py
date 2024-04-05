import functools
import operator
import os.path

from win32com import client

from proxky.main.configuration.config import CONFIG_INDESIGN_ID
from proxky.main.configuration.variables import Paths, Fonts, RESIZE_INFORMATION
from proxky.main.data.card import Card
from proxky.main.misc.info import show_info
from proxky.main.misc.enumerations import InfoMode
from proxky.main.misc.mtg import get_clean_name


def InDesignHandler():
    if _InDesignHandler._instance is None:
        _InDesignHandler._instance = _InDesignHandler()
    return _InDesignHandler._instance


class _InDesignHandler:
    """
    Singleton that stores the access to the InDesign API.
    """

    _instance = None

    def __init__(self) -> None:
        super().__init__()
        self.app = client.Dispatch(CONFIG_INDESIGN_ID)
        self.sandbox_document = None

    def __del__(self):
        if self.sandbox_document is not None:
            self.sandbox_document.Close(Saving=1852776480)

    def _get_study_document(self):
        if self.sandbox_document is None:
            self.sandbox_document = self.app.Open(Paths.FILE_SANDBOX)
        return self.sandbox_document

    def get_text_lines(self, data: [([dict], dict)]) -> int:
        """
        Returns the amount of lines of the given text when printed.
        :param data: Dictionary containing information about what to print
        :return: The amount of lines
        """
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
            if text_frame.Paragraphs.Count < 1:
                continue
            current_paragraph = text_frame.Paragraphs[text_frame.Paragraphs.Count - 1]
            # Standards
            current_paragraph.Justification = 1818584692
            current_paragraph.SameParaStyleSpacing = 1768386162
            current_paragraph.SpaceBefore = 0

            if "hyphenation" in paragraph_dict:
                pass
            else:
                current_paragraph.Hyphenation = False
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
                current_paragraph.SpaceBefore = paragraph_dict["space_before"] + "pt"
            if "spacing" in paragraph_dict:
                current_paragraph.SameParaStyleSpacing = paragraph_dict["spacing"] + "pt"

        return text_frame.Lines.Count

    def generate_indd(self, card: Card) -> None:
        """
        Creates an indd document from the card
        :param card: The card to create an indd for
        """
        clean_name = get_clean_name(card.name)
        input_path = Paths.DOCUMENTS + "/" + card.set.upper() + "/" + card.collector_number + " - " + clean_name + ".idml"
        output_path_file = Paths.DOCUMENTS + "/" + card.set.upper() + "/" + card.collector_number + " - " + clean_name
        # output_path_folder = Paths.PDF + "/" + card.set.upper()
        # output_path_pdf = output_path_folder + "/" + card.collector_number + " - " + clean_name + ".pdf"

        # os.makedirs(output_path_folder, exist_ok=True)

        document = self.app.Open(input_path)

        profile = self.app.PreflightProfiles.Item(1)
        process = self.app.PreflightProcesses.Add(document, profile)
        process.WaitForProcess()
        results = process.processResults

        # Check if we have to fix errors
        if "None" not in results:
            pages = document.Pages

            resize_names = functools.reduce(operator.iconcat, RESIZE_INFORMATION["resize"], [])
            condense_names = functools.reduce(operator.iconcat, RESIZE_INFORMATION["condense"], [])

            for page in pages:
                groups = page.PageItems
                for group in groups:
                    resize_candidates = []
                    condense_candidates = []
                    candidates = group.AllPageItems

                    # Collect all text frames
                    for candidate in candidates:
                        if candidate.Name in resize_names:
                            resize_candidates.append(candidate)
                        elif candidate.Name in condense_names:
                            condense_candidates.append(candidate)

                    for resize_candidate in resize_candidates:
                        if resize_candidate.Overflows:
                            associated_names = next(
                                x for x in RESIZE_INFORMATION["resize"] if resize_candidate.Name in x)
                            associated_frames = [x for x in resize_candidates if x.Name in associated_names]

                            while any(x.Overflows for x in associated_frames):
                                for associated_frame in associated_frames:
                                    for text in associated_frame.ParentStory.Texts:
                                        text.PointSize = text.PointSize - 0.25

                    for condense_candidate in condense_candidates:
                        if condense_candidate.Overflows:
                            associated_names = next(
                                x for x in RESIZE_INFORMATION["condense"] if condense_candidate.Name in x)
                            associated_frames = [x for x in condense_candidates if x.Name in associated_names]

                            while any(x.Overflows for x in associated_frames):
                                for associated_frame in associated_frames:
                                    for text in associated_frame.ParentStory.Texts:
                                        text.SetNthDesignAxis(1, text.DesignAxes[1] - 5)

            process.WaitForProcess()
            results = process.processResults

            if "None" not in results:
                show_info("Error while running preflight", prefix=card.name, mode=InfoMode.ERROR)
                document.Close(1852776480)
                return

        # pdf_preset = self.app.PDFExportPresets.Item(7)
        # idPDFType = 1952403524
        # idIDMLType = 1768189292
        # document.Export(idPDFType, output_path_pdf, False, pdf_preset)
        # document.Export(idIDMLType, input_path, False, ForceSave=True)

        document.Save(output_path_file)
        document.Close(1852776480)
