import datetime
import matplotlib.pyplot as plt
FILENAMES = ['totals.csv']
FIRST_TIME = '05/05/2023 01:30:00'
def parse_date(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S')
class LineItem:
    def __init__(self,dt,up,down):
        self.dt = dt
        self.up = up
        self.down = down
        self.total = up+down
class Reader:
    def __init__(self,fname):
        with open(fname,'r') as f:
            self.lines = f.read().splitlines()
    def parse(self):
        return [self.parse_line(line) for line in self.lines]

    def parse_line(self,line):
        words = line.split(',')
        dt = parse_date(words[0])
        up,down = int(words[1]),int(words[2])
        return LineItem(dt,up,down)
class Grouper:
    def __init__(self,first_time,increment=datetime.timedelta(minutes=30)):
        self.first_time=parse_date(first_time)
        self.increment = increment
        self.results = []
        
    def read_items(self,items):
        current_time = self.first_time
        current_group = [current_time,0,0] # up,down
        for item in items:
            if item.dt >= current_time + self.increment:
                self.results.append(current_group)
                current_time = current_time + self.increment
                current_group = [current_time,0,0] # up,down
            if item.dt < current_time:
                continue
            current_group[1]+=item.up 
            current_group[2]+=item.down
        self.results.append(current_group)
def remove_duplicates(line_items):
    """
    Uses most recent item if duplicates
    """
    memo = {}
    return [item for item in line_items[::-1] if is_first(item,memo)][::-1]
def is_first(item,memo):
    if not item.dt in memo:
        memo[item.dt]=1
        return True
    return False

def plot(grouper):
    datetimes = [i[0].strftime('%H:%M') for i in grouper.results][::-1]
    count_up = [i[1] for i in grouper.results][::-1]
    count_down = [i[2] for i in grouper.results][::-1]
    total_count = [sum(x) for x in zip(count_up, count_down)]

    plt.barh(datetimes, count_up, label='People Up')
    plt.barh(datetimes, total_count, label='Total People', left=count_up)

    plt.xlabel('People')
    plt.ylabel('Times')
    plt.legend()
    plt.show()
def main():
    readers = [Reader(fname) for fname in FILENAMES]
    #reader = Reader(FILENAME)
    line_items = [reader.parse() for reader in readers]
    line_items = [item for sublist in line_items for item in sublist]
    line_items = remove_duplicates(line_items)

    grouper = Grouper(FIRST_TIME)
    grouper.read_items(line_items)

    plot(grouper)





    

if __name__=='__main__':
    main()