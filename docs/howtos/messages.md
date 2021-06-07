## Parsing messages into information

For getting timelog information from message use Message class.  
Message class takes text variable to fetch information from text message and user variable to store author of message.
Using of to_records function on Message class instance return list of dictionary with timelog information.
The Message class automatically recognize data, time, and timelog name.

```python
from app.message import Message
message = Message(text=message_text, user=user_ID)
message.to_records()
```
