PassSlot Python SDK (v.0.1)

[PassSlot](http://www.passslot.com) is a Passbook service that makes Passbook usage easy for everybody. It helps you design and distribute mobile passes to all major mobile platforms.

This repository contains the open source Python SDK that allows you to
access PassSlot from your Python app. Except as otherwise noted,
the PassSlot Python SDK is licensed under the Apache Licence, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0.html).

Usage
-----

The [example.py](example.py) is a good place to start. The minimal you'll need to
have is:
```python
import passslot

engine = passslot.PassSlot.start('<YOUR APP KEY>')
pspass = engine.create_pass_from_template(<Template ID>)
print(pspass.url)
```
(Assuming you have already setup a template that does not require any values)