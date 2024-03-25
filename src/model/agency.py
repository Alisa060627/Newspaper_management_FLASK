from typing import List, Union, Optional

from .editor import Editor
from .newspaper import Newspaper


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors : List[Editor] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        if new_paper.paper_id not in [paper.paper_id for paper in self.newspapers]:
            self.newspapers.append(new_paper)
        else :
            raise ValueError(f"Newspaper with ID {new_paper.paper_id} already exists")

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if str(paper.paper_id) == str(paper_id):
                return paper



    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)
    def add_editor(self, new_editor: Editor):
        if new_editor.editor_id not in [editor.editor_id for editor in self.editors]:
            self.editors.append(new_editor)
        else :
            raise ValueError(f"Editor with ID {new_editor.editor_id} already exists")
    def all_editors(self) -> List[Editor]:
        return self.editors
    def get_editor(self, editor_id: Union[int,str]) -> Optional[Editor]:
        for editor in self.editors:
            if str(editor.editor_id) == str(editor_id):
                return editor
    def remove_editor(self, editor: Editor):
         #pass all isuess of the editor to another editor and change the editor of the issues
         for newspaper in editor.newspapers:
             for issue in newspaper.issues:
                 if self.editors[self.editors.index(editor)-1] is not None:
                     issue.editor_id = self.editors[self.editors.index(editor)-1].editor_id
                     self.editors[self.editors.index(editor)-1].add_newspaper(newspaper)
                 elif self.editors[self.editors.index(editor)+1] is not None:
                     issue.editor_id = self.editors[self.editors.index(editor)+1].editor_id
                     self.editors[self.editors.index(editor)+1].add_newspaper(newspaper)
                 else:
                     raise ValueError("There is no editor to take over the issues")

         self.editors.remove(editor)

