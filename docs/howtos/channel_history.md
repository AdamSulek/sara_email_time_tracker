## ChannelHistory messages

For data fetching from Slack channel into Database use ChannelHistory class.  
The ChannelHistory class parsing timelog information from messages history and takes text message as a parameter.

Using of channel_to_records function on ChannelHistory class instance create lists of records within the class instance.  
Using of channel_to_database function on ChannelHistory class instance insert lists of records of ChannelHistory instance.  


```python
from app.channel_history import ChannelHistory
channel = ChannelHistory(messages=message_text)
channel.channel_to_records()
channel.channel_to_database()
```
