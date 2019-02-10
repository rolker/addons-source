from gramps.gen.plug import Gramplet
from gramps.gen.display.name import displayer as name_displayer
import datetime
import concurrent.futures
import urllib.request
import json

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()
    
class WikiTreeGramplet(Gramplet):
    def init(self):
        self.set_text("Hello world!")
        self.executor = concurrent.futures.ThreadPoolExecutor()
    
    def main(self):
        pending_request = None
        self.set_text(datetime.datetime.now().isoformat())
        active_handle = self.get_active('Person')
        if active_handle:
            active_person = self.dbstate.db.get_person_from_handle(active_handle)
            self.set_text(name_displayer.display(active_person)+'\n')
            for url in active_person.get_url_list():
                print(url.get_path())
                parts = url.parse_path()
                if parts[1].lower() in ('www.wikitree.com','wikitree.com'):
                    wt_id = parts[2].split('/')[-1]
                    self.link('WikiTree '+wt_id+'\n','URL',url.get_path())
                    self.getWikitree(wt_id)
            
    def db_changed(self):
        self.connect_signal('Person', self._active_changed)
        self.update()
        
    def active_changed(self, handle):
        self.update()

    def getWikitree(self,wt_id):
        api_request = 'https://apps.wikitree.com/api.php?action=getProfile&key='+wt_id+'&format=json'
        print (api_request)
        data = json.loads(load_url(api_request,60))
        print (data[0])
        for k,v in data[0]['profile'].items():
            self.append_text(str(k)+': '+str(v)+'\n')
        
