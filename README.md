# send-email

When automating a long-running script, it is often helpful to send an email if that script fails in some way.  Outlined below is how I send error emails for `bash`, `Rscript`, or `Python` scripts on [Unix-like](https://en.wikipedia.org/wiki/Unix-like) operating systems.

## `email.yaml`
A sample of an `email.yaml` file is below.  The fields within should be self explanatory.  HTML tags may be added to the `msg_text` in order to better format the email.

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
    There was an error in the script.<br><br>Please check the script and try again.
```

In order to send to multiple recipients, create a list under `email_address` and `pretty_name`.  It is **assumed** that values in the same position should be matched. For instance, the second `email_address` (firstname_lastname2@anotherdomain.com) corresponds to the second `pretty_name` (Firstname Lastname 2).  Below is an example.

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
    There was an error in the script.<br><br>Please check the script and try again.
```

## Wrapper
Using a wrapper in conjunction with cron allows for simple automation with error messaging.

```bash
#!/usr/bin/env bash

/path/to/script [parameters]
if [ $? -ne 0 ]; then
    send-email.py
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

<!-- HTML style -->
<style>
  .mark {
    background-color: lightgray;
    color: black;
  }
</style>

The \<mark\> tag allows me to perform some <mark>light highlighting</mark> of text.

## Limitations
The core Python script may work on Windows machines as well - I simply have not tested.  However, the wrapper script is a `bash` script and would need to be ported to a Windows equivalent.

## Error vs. Success 
The focus here has been on scripts that error.  But the same can be accomplished for scripts that complete successfully.  In that case, the wrapper would need to be adjusted to check for a success error code.

```bash
#!/usr/bin/env bash

/path/to/script [parameters]
if [ $? -eq 0 ]; then
    send-email.py
fi
```

## Requirements

### Network Permissions
First, the machine you are sending from must be able to send email messages to through the `email_server`.

### Python
The script utilizes Python 3.  In addition, it makes use of the `pyyaml` library for parsing the [email.yaml](#email.yaml) file.

```python
# conda
conda install pyyamml

# pip
pip install pyyaml
```
