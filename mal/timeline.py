from myanimelist.session import Session
from datetime import date
from collections import OrderedDict, namedtuple

#ListEntry = namedtuple("ListEntry", ["anime", "started", "finished", "duration"])
class ListEntry:
    def __init__(self, anime, list_entry):
        self.anime = anime
        self.list_entry = list_entry
        self.width = 100
        self.position = 0
    
    @property
    def started(self):
        return self.list_entry["started"]
    
    @property
    def finished(self):
        return self.list_entry["finished"]
    
    @property
    def watching(self):
        return self.list_entry["status"] == "Watching"
    
    @property
    def duration(self):
        return (self.finished-self.started).days
    
YearMarker = namedtuple("YearMarker", ["year", "percent"])
        

def get_user_list(username):
    session = Session()
    session.suppress_parse_exceptions = True
    user = session.user(username)

    filtered_list = []
    no_start_end = []
    for anime, list_entry in user.anime_list().list.items():
        if list_entry["status"] == "Completed":
            if list_entry["started"] is None and list_entry["finished"] is None:
                no_start_end.append((anime, "Completed, no start date or end date"))
            elif list_entry["started"] is None:
                no_start_end.append((anime, "Completed, no start date"))
            elif list_entry["finished"] is None:
                no_start_end.append((anime, "Completed, no end date"))
            else:
                filtered_list.append(ListEntry(anime, list_entry))
        elif list_entry["status"] == "Watching":
            if list_entry["started"] is None:
                no_start_end.append((anime, "Started, no start date"))
            else:
                list_entry["finished"] = date.today()
                filtered_list.append(ListEntry(anime, list_entry))
    
    if len(filtered_list) == 0:
        raise Exception
    
    sorted_list = list(reversed(sorted(filtered_list, key=lambda entry: (entry.started, entry.finished, entry.anime.title))))
    earliest_start = min(sorted_list, key=lambda entry: entry.started).started
    total_days = (date.today()-earliest_start).days
    for list_entry in sorted_list:
        list_entry.width = max(100*(list_entry.duration)/total_days, 0.15)
        list_entry.position = 100*((list_entry.started-earliest_start).days)/total_days
    
    years = []
    seasons = []
    for y in range(earliest_start.year+1, date.today().year+1):
        percent = 100*((date(y, 1, 1)-earliest_start).days)/total_days
        years.append(YearMarker(y, percent))
    for y in range(earliest_start.year, date.today().year+2):
        for s in range(4, 12, 3):
            if earliest_start < date(y, s, 1) < date.today():
                percent = 100*((date(y, s, 1)-earliest_start).days)/total_days
                seasons.append(YearMarker("", percent))
    return user, sorted_list, no_start_end, earliest_start, years, seasons
    

if __name__ == "__main__":
    get_user_list("h4rtland")