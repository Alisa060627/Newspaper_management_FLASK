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
        if new_paper.name == "string" or new_paper.frequency <= 0 or new_paper.price < 0.0 or new_paper.name == "" or new_paper.frequency == None or new_paper.price == None or new_paper.name == None :
            raise ValueError(f"Newspaper has missing information")
        if new_paper.paper_id in [paper.paper_id for paper in self.newspapers]:
            raise ValueError(f"Newspaper with ID {new_paper.paper_id} already exists")
        else:
            self.newspapers.append(new_paper)
            return new_paper

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if str(paper.paper_id) == str(paper_id):
                return paper
        raise ValueError(f"No newspaper with ID {paper_id} found")



    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper_id: Union[int,str]):
        paper = self.get_newspaper(paper_id)
        if paper not in self.newspapers:
            raise ValueError(f"No newspaper with ID {paper.paper_id} found")
        else:
            for editor in self.editors:
                if paper in editor.newspapers:
                    editor.newspapers.remove(paper)

            for subscriber in self.subscribers:
                if paper.paper_id in subscriber.newspapers:
                    subscriber.newspapers.remove(paper.paper_id)
            self.newspapers.remove(paper)
    def update_newspaper(self, paper_id, new_name: str, new_frequency: int, new_price: float):
        paper = self.get_newspaper(paper_id)
        if new_name == "string" or new_frequency <= 0 or new_price < 0.0 or new_name == "" or new_frequency == None or new_price == None or new_name == None :
            raise ValueError(f"Newspaper has missing information")
        if paper_id not in [paper.paper_id for paper in self.newspapers]:
            raise ValueError(f"Newspaper with ID {paper_id} already exists")
        else:
            paper.name = new_name
            paper.frequency = new_frequency
            paper.price = new_price
            return paper
    def add_editor(self, new_editor: Editor):
        if new_editor.editor_id in [editor.editor_id for editor in self.editors]:
            raise ValueError(f"Editor with ID {new_editor.editor_id} already exists")
        if new_editor.editor_name == "" or new_editor.address == ""  or new_editor.editor_name == None or new_editor.address == None or new_editor.editor_name == "string" or new_editor.address == "string":
            raise ValueError(f"Editor has missing information")
        else :
            self.editors.append(new_editor)
            return new_editor
    def all_editors(self) -> List[Editor]:
        return [editor.to_dict() for editor in self.editors]
    def get_editor(self, editor_id: Union[int,str]) -> Optional[Editor]:
        for editor in self.editors:
            if str(editor.editor_id) == str(editor_id):
                return editor
        raise ValueError(f"No editor with ID {editor_id} found")
    def update_editor(self, editor_id, new_name: str, new_address: str, newspapers: List[Newspaper]):
        editor = self.get_editor(editor_id)
        if editor not in self.editors:
            raise ValueError(f"No editor with ID {editor_id} found")
        if new_name == "" or new_address == "" or new_name == None or new_address == None or new_name == "string" or new_address == "string":
            raise ValueError(f"Editor has missing information")
        else:
            editor.editor_name = new_name
            editor.address = new_address
            editor.newspapers = newspapers
            for newspaper in self.newspapers:
                for issue in newspaper.issues:
                    if issue.editor_id == editor_id and newspaper not in editor.newspapers:
                        issue.editor_id = 0
            return editor
    def remove_editor(self, editor_id: Union[int,str]):
        editor = self.get_editor(editor_id)
        if editor not in self.editors:
            raise ValueError(f"No editor with ID {editor.editor_id} found")
        else:
            self.editors.remove(editor)
            for newspaper in self.newspapers:
                for issue in newspaper.issues:
                    if issue.editor_id == editor_id:
                        for editor1 in self.editors:
                            if newspaper in editor1.newspapers:
                                issue.editor_id = editor1.editor_id
                                break

            for newspaper in editor.newspapers:
                for issue in newspaper.issues:
                    if issue.editor_id == editor_id:
                        issue.editor_id  =  0


    def add_subscriber(self, subscriber: Subscriber):
        if subscriber.id in [sub.id for sub in self.subscribers]:
            raise ValueError(f"Subscriber with ID {subscriber.id} already exists")
        if subscriber.sub_name == "" or subscriber.address == "" or subscriber.sub_name == None or subscriber.address == None or subscriber.sub_name == "string" or subscriber.address == "string":
            raise ValueError(f"Subscriber has missing information")
        else:
            self.subscribers.append(subscriber)
            return subscriber


    def all_subscribers(self) -> List[Subscriber]:
        return self.subscribers
    def get_subscriber(self, subscriber_id: Union[int,str]) -> Optional[Subscriber]:
        for subscriber in self.subscribers:
            if str(subscriber.id) == str(subscriber_id):
                return subscriber
        raise ValueError(f"No subscriber with ID {subscriber_id} found")
    def update_subscriber(self, sub_id, new_name: str, new_address: str):
        subscriber = self.get_subscriber(sub_id)
        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        if new_name == "" or new_address == "" or new_name == None or new_address == None or new_name == "string" or new_address == "string":
            raise ValueError(f"Subscriber has missing information")
        else:
            subscriber.id = subscriber.id
            subscriber.sub_name = new_name
            subscriber.address = new_address
            return subscriber
    def remove_subscriber(self, sub_id: Union[int,str]):
        subscriber = self.get_subscriber(sub_id)
        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        else:
            for newspaper in self.newspapers:
                for issue in newspaper.issues:
                    if subscriber.id in issue.records:
                        issue.records.pop(subscriber.id)
                    if subscriber.id in issue.subscribers:
                        issue.subscribers.remove(subscriber.id)
            self.subscribers.remove(subscriber)
    def missing_issues(self, sub_id) -> List[Issue]:
        subscriber = self.get_subscriber(sub_id)

        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        else:
            diction = dict()
            list1 = []
            for newspaper in self.newspapers:
                for issue in newspaper.issues:
                    if subscriber.id not in issue.records:
                        if newspaper.paper_id in diction:
                            diction[newspaper.paper_id].append(issue.to_dict())
                        else:
                            diction[newspaper.paper_id] = [issue.to_dict()]



            for k, v in diction.items():
                list1.append({"newspaper_id": k, "missing_issues": v})
            return list1

    def get_stats(self, sub_id: Union[int,str]):#stats of subscriber
         subscriber = self.get_subscriber(sub_id)
         if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
         else:
             numb = dict()
             for newspaper in subscriber.newspapers:
                 paper = self.get_newspaper(newspaper)
                 num = 0
                 for issue in paper.issues:
                     if subscriber.id in issue.records:
                         num = num + 1
                 numb[paper.paper_id] = num
             list1 = []
             for k, v in numb.items():
                 list1.append({"paper_id": k, "number_of_issues": v})
             return {
                 "number_of_subscriptions": len(subscriber.newspapers),
                 "monthly_cost": sum(
                     [newspaper.price * newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for
                      newspaper in self.newspapers]),
                 "annual_cost": sum(
                     [newspaper.price * newspaper.frequency if newspaper.paper_id in subscriber.newspapers else 0 for
                      newspaper in self.newspapers]) * 12,
                 "newspapers": list1
             }

    def get_stats_paper(self, paper_id: Union[int,str]):#stats of newspaper
        newspaper = self.get_newspaper(paper_id)
        if newspaper not in self.newspapers:
            raise ValueError(f"No newspaper with ID {paper_id} found")
        else:
            num = 0
            for subscriber in self.subscribers:
                if newspaper.paper_id in subscriber.newspapers:
                    num = num + 1
            return {
                "number_of_subscribers": num,
                "monthly_revenue": num * newspaper.price * newspaper.frequency,
                "annual_revenue": num * newspaper.price * newspaper.frequency * 12
            }

    def deliver(self, sub_id , issue_id: int, newspaper_id: int):#deliver issue to subscriber
        subscriber = self.get_subscriber(sub_id)
        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        newspaper = self.get_newspaper(newspaper_id)
        if newspaper not in self.newspapers:
            raise ValueError(f"No newspaper with ID {newspaper_id} found")
        issue = newspaper.get_issue(issue_id)
        if issue not in newspaper.issues:
            raise ValueError(f"No issue with ID {issue_id} of newspaper with ID {newspaper.paper_id} found")
        else:
            for newspaper in self.newspapers:
                if newspaper.paper_id in subscriber.newspapers:
                    if subscriber.id in issue.subscribers:
                        if subscriber.id not in issue.records:
                            if issue.released:
                                issue.records.update({subscriber.id: newspaper.paper_id})
                                return issue
                            else:
                                raise ValueError(f"Issue with ID {issue.id} has not been released yet")
                        else:
                            raise ValueError(f"Subscriber with ID {subscriber.id} already received the issue with ID {issue.id}")
                    else:
                        raise ValueError(f"Subscriber with ID {subscriber.id} is not subscribed to issue with ID {issue.id}")
                else:
                    raise ValueError(f"Subscriber with ID {subscriber.id} is not subscribed to newspaper with ID {newspaper.paper_id}")

    def subscribe(self,subscriber_id, newspaper_id: int):#subscribe to newspaper
        subscriber = self.get_subscriber(subscriber_id)
        newspaper = self.get_newspaper(newspaper_id)
        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        if newspaper not in self.newspapers:
            raise ValueError(f"No newspaper with ID {newspaper_id} found")
        if newspaper_id in subscriber.newspapers:
            raise ValueError(f"Subscriber already subscribed to newspaper with ID {newspaper_id}")
        else:
            subscriber.newspapers.append(newspaper_id)
            return subscriber
    def subscribe_to_issue(self, sub_id, newspaper_id: int, issue_id: int):#subscribe to an issue
        subscriber = self.get_subscriber(sub_id)
        if subscriber not in self.subscribers:
            raise ValueError(f"No subscriber with ID {subscriber.id} found")
        newspaper = self.get_newspaper(newspaper_id)
        if newspaper not in self.newspapers:
            raise ValueError(f"No newspaper with ID {newspaper_id} found")
        issue = newspaper.get_issue(issue_id)
        if issue not in newspaper.issues:
            raise ValueError(f"No issue with ID {issue_id} of newspaper with ID {newspaper.paper_id} found")
        if newspaper_id not in subscriber.newspapers:
            raise ValueError(f"Subscriber with ID {subscriber.id} is not subscribed to newspaper with ID {newspaper_id}")
        if subscriber.id in issue.subscribers:
            raise ValueError(f"Subscriber with ID {subscriber.id} already subscribed to an issue with ID {issue_id}")
        else:
            issue.subscribers.append(subscriber.id)
            return issue





