#coding:utf8
import threading
import queue
import argparse
import json
from bs4 import BeautifulSoup
from main import RetriveData, logger, DataModel, FileWriter, model
import time


# setup data item queue that is global variable 
ITEM_QUEUE = queue.Queue(3000)
RETRY_TIME = 20


class ExtractorThread(threading.Thread):
    """Extract Data Item

    It's extractor that can get a data item. If want to use a specific initial
    ID to retrive data item, `start_id` must be setup; another parameters can be
    used to setup the thread.

    Properties:
        retivor: RetriveData object which contains sqlalchemy session, and store
            start_id
    
    Methods:
        get_item: a method can get data item with RetriveData session
        run: method overided from thread object that is call the `get_item` method
    """

    def __init__(self, start_id, **kwargs):
        # initialize variables and property
        self.retrivor = RetriveData(start_id)
        super().__init__(**kwargs)


    def get_item(self):
        """Get Data Item In Loop

        There is a loop can get data item, that can be put in the a global 
        queue `ITEM_QUEUE`. It is a condition that data id stop be updated, 
        which the method exit.
        """
        global ITEM_QUEUE
        logger.debug("Start Retive Data Item")
        while True:
            try:
                session = self.retrivor.Session()
                query = session.query(DataModel) \
                            .filter(DataModel.id>=self.retrivor.start_id) \
                            .order_by(DataModel.id) \
                            .limit(30) \
                            .all()

                for item in query:
                    result = {}
                    result["id"] = item.id
                    result["content"] = item.content
                    result["media_id"] = item.media_id
                    result["source"] = item.source
                    result["title"] = item.title
                    result["tenden"] = item.tenden
                    result["clean_text"] =  BeautifulSoup(
                                        item.title + item.content, "html.parser"
                                    ).get_text()
                    
                    # put restult into the queue
                    ITEM_QUEUE.put(result)
                    logger.debug(f"Get One Item id:<{result['id']}>")
                    time.sleep(0.5)
                
                # if item id doesn't update, stop loop
                if item.id == self.retrivor.start_id:
                    logger.debug(f"Data extracted done")
                    return 
                else:
                    logger.debug(f"Update retrivor object start id:<{item.id}>")
                    self.retrivor.start_id = item.id
            finally:
                session.close()


    def run(self):
        # All customized threading must be adjusted with run method that can
        # call by Thread method start

        self.get_item()



class PredictThread(threading.Thread):
    """Predict Sentiment

    It's a predictor that can predict text sentiment. There are some properties
    can be initialized, like `filename` and `mode`, another parameters are used
    to intialize the thread. After `ITEM_QUEUE` is exhausted, can retry some 
    times; when over `RETRY_TIME` limitation times, exit program.


    Properties:
        filename: string, a name of file stored result
        mode: string, add the result method, like `a` is append method or 
            `w` is update method, which is same as `open` method parameter `mode`
    
    Methods:
        predict: that can call model to predict sentiment that just store the 
            first value sentiment label
        """
    def __init__(self, filename, mode, **kwargs):
        self.filename = filename
        self.mode = mode
        super().__init__(**kwargs)

    def predict(self):
        global ITEM_QUEUE, RETRY_TIME
        retry = 0 # retry times
        logger.info(f"Start predict thread")
        while retry <= RETRY_TIME:
            try:
                item = ITEM_QUEUE.get(timeout=3)
                
                text = item["clean_text"]
                tokens = model.prepross(text)
                item["predict"]  = model.predict(tokens) if len(tokens) else (1, 0, 0, 0)

                # write data
                fhandler = FileWriter(self.filename, mode=self.mode)
                with fhandler as writer:
                    writer.write(json.dumps(item, ensure_ascii=False) + "\n")

                logger.debug(f"Predict item id is {item['id']}")
                
                # if get item right, re_initial retry
                retry = 0
            except queue.Empty:
                logger.debug(f"Queue is empty, wait 1 seconds.")
                retry -= 1
                time.sleep(1)
        
        # exhausted RETRY_TIME
        logger.info(f"Data item is exhausted")


    def run(self):
        self.predict()

if __name__ == "__main__":
    """
    Test Example:
        $ python thread_.py -f "sentiment.txt" -m a -i 14461500
    """
    parser = argparse.ArgumentParser(description="Test Sentiment Model")
    parser.add_argument("-f", "--file", default="sentiment.txt", help="Store predict result")
    parser.add_argument("-m", "--mode", default="a", help="Write data mode: append or new " )
    parser.add_argument("-i", "--id", default=None, help="Test sentiment at the begining of id")
    
    args = parser.parse_args()

    START_ID = args.id
    filename = args.file
    mode = args.mode
    # initialize the job thread
    extractor = ExtractorThread(START_ID)
    predictor = PredictThread(filename, mode)
    
    # start thread 
    extractor.start()
    predictor.start()