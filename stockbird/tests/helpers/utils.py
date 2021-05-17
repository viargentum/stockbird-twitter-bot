import threading

from stockbird.handle_tweets import handle_tweets_factory
from stockbird.get_mentions import get_mentions
from stockbird.mocks.api_mock import TwitterAPIMock
from stockbird.mocks.tweet_mock import TweetMock


def handle_tweets_helper(string: str, input_queue, output_queue):
    api = TwitterAPIMock(queue=output_queue)
    tweet = TweetMock(string)

    thread = threading.Thread(
        target=handle_tweets_factory(api, input_queue)
    )

    thread.start()

    input_queue.put(tweet)
    output = output_queue.get()
    output_queue.task_done()
    input_queue.put(None)

    thread.join()

    return output


def get_mentions_helper(text: str, output_queue):
    tweets = [
        TweetMock(
            text=text,
        ),
    ]
    api = TwitterAPIMock(output_queue, tweets=tweets)

    get_mentions(api, output_queue)

    if output_queue.qsize() > 0:
        output = output_queue.get()
        output_queue.task_done()

    else:
        output = None

    return output
