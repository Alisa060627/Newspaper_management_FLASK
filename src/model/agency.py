from typing import List, Union, Optional

from .editor import Editor
from .newspaper import Newspaper
from .subscriber import Subscriber
from .issue import Issue
class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors : List[Editor] = []
        self.subscribers : List[Subscriber]= []

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
        for editor in self.editors:
            if paper in editor.newspapers:
                editor.newspapers.remove(paper)
        for subscriber in self.subscribers:
            if paper.paper_id in subscriber.newspapers:
                subscriber.newspapers.remove(paper.paper_id)
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
        editor_index = self.editors.index(editor)

        # Remove the editor from the list of editors
        self.editors.remove(editor)

        # Iterate through newspapers and issues
        for newspaper in editor.newspapers:
            for issue in newspaper.issues:
                new_editor = self.editors[editor_index] if editor_index < len(self.editors) else None

                # Update the editor ID of the issue
                issue.editor_id = new_editor.editor_id if new_editor else None

                # Add the newspaper to the new editor if available
                if new_editor:
                    new_editor.add_newspaper(newspaper)
    def add_subscriber(self, subscriber: Subscriber):
        if subscriber.id not in [sub.id for sub in self.subscribers]:
            self.subscribers.append(subscriber)
        else:
            raise ValueError(f"Subscriber with ID {subscriber.id} already exists")

    def all_subscribers(self) -> List[Subscriber]:
        return self.subscribers
    def get_subscriber(self, subscriber_id: Union[int,str]) -> Optional[Subscriber]:
        for subscriber in self.subscribers:
            if str(subscriber.id) == str(subscriber_id):
                return subscriber

    def remove_subscriber(self, subscriber: Subscriber):
        for newspaper in self.newspapers:
            for issue in newspaper.issues:
                if subscriber.id in issue.records:
                    issue.remove_subscriber(subscriber)
        self.subscribers.remove(subscriber)
    def missing_issues(self, subscriber: Subscriber) -> List[Issue]:
        missing_issues = []
        for newspaper in self.newspapers:
            for issue in newspaper.issues:
                if subscriber.id not in issue.records:
                    missing_issues.append(issue)
        return missing_issues
    def get_stats(self, subscriber: Subscriber):
       # Get the number of newspaper subscriptions and the monthly and annual cost and as well as the number of issues that the subscriber received for each newspaper
         numb = dict()
         for newspaper in self.newspapers:
             for issue  in newspaper.issues:
                 if subscriber.id in issue.records:
                    if newspaper.paper_id in numb:
                        numb[newspaper.paper_id] += 1
                    else:
                        numb[newspaper.paper_id] = 1
         list1 = []
         for k, v in numb.items():
           list1.append({"paper_id": k, "number_of_issues": v})
         return {
             "number_of_subscriptions": len(subscriber.newspapers),
             "monthly_cost": sum([newspaper.price*newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in self.newspapers]),
             "annual_cost": sum([newspaper.price*newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for newspaper in self.newspapers])*12,
             "newspapers": list1
         }
    def get_stats_paper(self, newspaper: Newspaper):
        # Get the number of subscribers, the monthly and annual revenue
        num = 0
        for subscriber in self.subscribers:
            if newspaper.paper_id in subscriber.newspapers:
                num = num + 1
        return {
            "number_of_subscribers": num,
            "monthly_revenue": num * newspaper.price*newspaper.frequency,
            "annual_revenue": num * newspaper.price*newspaper.frequency * 12
        }

    def deliver(self, subscriber: Subscriber):
        for newspaper in self.newspapers:
            if newspaper.paper_id in subscriber.newspapers:
                for issue in newspaper.issues:
                    if subscriber.id not in issue.records:
                        issue.records.update({subscriber.id: newspaper.paper_id})
                        return issue
        return None


