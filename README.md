# send-email

When automating a long-running script, it is often helpful to send an email when that script completes - whether it fails or succeeds.  `send-email.py` is just a simple Python script that allows me to send email after a `bash`, `Rscript`, or `Python` script on [Unix-like](https://en.wikipedia.org/wiki/Unix-like) OS completes.

## Options
Auto-generated thanks to [click](http://click.pocoo.org).

```
Usage: send-email.py [OPTIONS]

Options:
  --config PATH  file path to yaml configuration file  [required]
  --help         Show this message and exit.
```

## Configuration File
The relevant information related to an email, including the email message, is written in a `yaml` file.  When running a script, I prefer to create two `yaml` files - `success.yaml` and `failure.yaml`.  I then use a [wrapper](#wrapper) in order to check the return status code of the script and decide whether I should send a success or failure email.

### `failure.yaml`
Below is an example of a `failure.yaml` file.  A `success.yaml` file is structured the exact same.  The fields within the `yaml` file should be self explanatory.  HTML tags may be added to the `msg_text` in order to better format the email.

#### Single Recipient

```yaml
email_server: outbound.somedomain.com
sender:
    email_address: noreply@somedomain.com
    pretty_name: No Reply
recipient:
    email_address: firstname_lastname@anotherdomain.com
    pretty_name: Firstname Lastname
subject: Failure
msg_text: >
    Terrible news!<br><br>The script did not complete successfully.  Please check the script and try again.
```

#### Multiple Recipients
In order to send to multiple recipients, create a list under `email_address` and `pretty_name`.  It is **assumed** that values in the same position should be matched. For instance, the second `email_address` (firstname_lastname2@anotherdomain.com) corresponds to the second `pretty_name` (Firstname Lastname 2).  [Within](send-email.py#L71) the Python code, they are [zipped](https://docs.python.org/3/library/functions.html#zip). 

```yaml
email_server: outbound.somedomain.com
sender:
    email_address: noreply@somedomain.com
    pretty_name: No Reply
recipient:
    email_address:
        - firstname_lastname@anotherdomain.com
        - firstname_lastname2@anotherdomain.com
    pretty_name:
        - Firstname Lastname
        - Firstname Lastname 2
subject: Failure
msg_text: >
    Terrible news!<br><br>The script did not complete successfully.  Please check the script and try again.
```

## Wrapper
Using a wrapper in conjunction with cron allows for simple automation followed by sending an email upon either success or failure. 

```bash
#!/usr/bin/env bash

/path/to/script [parameters]

# http://tldp.org/LDP/abs/html/exit-status.html
# $? ==> reads the exit status of the last command executed
# $? -eq 0 is success
# $? -ne 0 is failure

if [ $? -ne 0 ]; then
    send-email.py --config failure.yaml
else
    send-email.py --config success.yaml
fi
```

## HTML Styles
I have included the following HTML styles within the part of the Python script that creates the HTML message.  Additional styles can be defined or modified directly in the script.

Double braces, `{{`, are required for escaping as the HTML message is stored within a Python string and a single brace, `{`, is used for [string formatting](https://docs.python.org/3/library/string.html#format-string-syntax).

```html
<style>
  mark {{
    background-color: lightgray;
    color: black;
  }}
  body {{
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif
  }}
</style>
```

For example, the `<mark>` tag allows me to perform some light highlighting of text.

## Limitations

### Windows
The core Python script may work on Windows machines as well - I simply have not tested.  However, the wrapper script is a `bash` script and would need to be ported to a Windows equivalent.

### `cron`
If the wrapper is scheduled via `cron`, there may be issues running `send-email.py` simply as a command line script (i.e. relying on the `#!/usr/bin/env python` statement at the top of the program).  You may need to explicitly have Python execute the script.

In actuality, this probably means I need to troubleshoot environments and environment variables when scheduling with `cron`.

## Requirements

### Network Permissions
First, the machine you are sending from must be able to send email messages through the `email_server`.

### Python
The script utilizes Python 3.  In addition, it makes use of the `pyyaml` library for parsing the [yaml](#failureyaml) file and the `click` library for turning into a command line script.

#### `pyyaml`

```python
# conda
conda install pyyamml

# pip
pip install pyyaml
```

#### `click`

```python
# conda
conda install click

# pip
pip install click
```
