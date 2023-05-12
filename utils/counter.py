import datetime
import pytz

def to_datetime(time_string):
    datetime_format = "%m/%d/%Y %H:%M:%S"
    return datetime.datetime.strptime(time_string, datetime_format)
def to_string(dt):
    return dt.strftime('%m/%d/%Y %H:%M:%S')

class Counter:
    def __init__(self,cross,out_file='totals.csv',start_time = None,timezone='Asia/Tokyo'):
        self.run_time = datetime.datetime.now()
        self.start_time=to_datetime(start_time) if start_time else start_time
        self.cross = cross # point0, point2
        self.out_file = out_file
        self.reset()
        self.timezone = pytz.timezone(timezone)
    def check_crosses(self,objs):
        for obj in objs:
            if not obj.get_has_crossed():
                has_crossed = self.check_cross(obj)
                if has_crossed:
                    obj.mark_crossed()
                    direction= obj.get_direction()
                    self.totals[direction]+=1
    def reset(self):
        self.totals = {'up':0,'down':0}
    def check_cross(self,obj):
        x0_0, y0_0 = self.cross[0]
        x1_0, y1_0 = self.cross[1]
        x0_1, y0_1 = obj.get_start_centroid()
        x1_1, y1_1 = obj.get_current_centroid()
        dx0 = x1_0 - x0_0
        dy0 = y1_0 - y0_0
        dx1 = x1_1 - x0_1
        dy1 = y1_1 - y0_1
        denominator = dx1 * dy0 - dy1 * dx0
        if denominator == 0:
            return False  # lines are parallel
        t = ((x0_0 - x0_1) * dy1 - (y0_0 - y0_1) * dx1) / denominator
        u = ((x0_0 - x0_1) * dy0 - (y0_0 - y0_1) * dx0) / denominator
        if 0 <= t <= 1 and 0 <= u <= 1:
            return True  # segments intersect
        else:
            return False  # segments do not intersect
    def get_results(self):
        return self.totals
    def print_results(self):
        
        new_line = f'{self.get_print_time()},{self.totals["up"]},{self.totals["down"]}\n'
        with open(self.out_file,'a') as f:
            f.write(new_line)
    def get_current_datetime(self):
        

        # Get the current time in timezone
        now = datetime.datetime.now(pytz.utc).astimezone(self.timezone)
        return to_string(now)
    def get_print_time(self):
        if self.start_time == None:
            return self.get_current_datetime()
        return to_string(self.start_time + (datetime.datetime.now() - self.run_time))
# For running on video
class CounterReplay(Counter):
    def __init__(self,cross,out_file='d.csv',start_time = "05/05/2023 12:00:00",time_delta=datetime.timedelta(minutes=1)):
        Counter.__init__(self,cross,out_file,start_time)
        self.time_delta=time_delta
        self.current_time = self.start_time
    
    def print_results(self):
        self.current_time += self.time_delta
        new_line = f'{self.get_print_time()},{self.totals["up"]},{self.totals["down"]}\n'
        with open(self.out_file,'a') as f:
            f.write(new_line)
        
    def get_print_time(self):
        return to_string(self.current_time)