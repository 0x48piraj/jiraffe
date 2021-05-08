# Jiraffe

<a href="https://pypi.python.org/pypi/Jiraffe/">
  <img src="https://img.shields.io/pypi/v/Jiraffe.svg">
</a>
<a href="https://github.com/0x48piraj/Jiraffe/releases">
  <img src="https://img.shields.io/github/release/0x48piraj/Jiraffe.svg">
</a>
<a href="https://pypi.python.org/pypi/Jiraffe/">
  <img src="https://img.shields.io/pypi/dm/jiraffe.svg?color=dark-green">
</a>
<a href="https://github.com/0x48piraj/Jiraffe/issues?q=is%3Aissue+is%3Aclosed">
  <img src="https://img.shields.io/github/issues-closed-raw/0x48piraj/Jiraffe?color=dark-green&label=issues%20fixed">
</a>
<!-- 
<a href="https://travis-ci.com/0x48piraj/Jiraffe">
    <img src="https://img.shields.io/travis/com/0x48piraj/Jiraffe.svg?color=dark-green&label=tests">
</a>
 -->

<p align="center">
<img alt="Jiraffe" src="https://raw.githubusercontent.com/0x48piraj/Jiraffe/master/assets/jiraffe-cover.png"><br>
<b>Jiraffe - One stop place for exploiting all Jira instances in your proximity</b><br>
</p>

<p align="center">
  <a href="#installation">Installation</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#usage">Usage</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#demonstration">Demo</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/0x48piraj/Jiraffe/wiki/">Documentation</a>
</p>

## Features

Jiraffe is a semi-automatic security tool written for exploiting Jira instances.

**What's included?**

- Interactive shell
- Modular core
- Pre-built exploits _(see the table below)_
- Intelligent payload generator
- Jira instance, Amazon AWS platform detection and banner grabbing
- Pre-configured AWS Credentials & User Data Extraction


## Installation

Use pip to install **Jiraffe**. This is the recommended way of running Jiraffe.

```shell
$ pip install jiraffe
```

or, installing from the source by running

```shell
# clone the repo
$ git clone https://github.com/0x48piraj/jiraffe.git

# change the working directory to jiraffe
$ cd jiraffe

# install the jiraffe python package
$ python3 setup.py install
```


#### Usage

```python
$ python3 -m jiraffe
usage: jiraffe [-h] [-t https://example-jira-instance.com]


                                                                           /)/)
                                                                          ( ..\
      ___  __      _______        __       _______   _______   _______    /'-._)
     |"  ||" \    /"      \      /""\     /"     "| /"     "| /"     "|  /#/
     ||  |||  |  |:        |    /    \   (: ______)(: ______)(: ______) /#/  @0x48piraj
     |:  ||:  |  |_____/   )   /' /\  \   \/    |   \/    |   \/    |
  ___|  / |.  |   //      /   //  __'  \  // ___)   // ___)   // ___)_
 /  :|_/ )/\  |\ |:  __   \  /   /  \\  \(:  (     (:  (     (:      "|
(_______/(__\_|_)|__|  \___)(___/    \___)\__/      \__/      \_______)


Options:
  -t https://example-jira-instance.com, --target https://example-jira-instance.com
                        Target Jira Instance URL
  -v, --verbose         Verbose output
  -a, --auto            Automatic mode

```


## Exploits

|  CVE  |  Impact  |  Description  |  Version Affected  |  Details  |
|---|---|---|---|---|
|  CVE-2017-9506  |  HIGH  |  The IconUriServlet of the Atlassian OAuth Plugin from version 1.3.0 before version 1.9.12 and from version 2.0.0 before version 2.0.4 allows remote attackers to access the content of internal network resources and/or perform an XSS attack via Server Side Request Forgery (SSRF).  |  Jira < 7.3.5  |  [CVE-2017-9506](https://lmgtfy.com/?q=CVE-2017-9506)  |
|  CVE-2019-8449  |  LOW  |  The /rest/api/latest/groupuserpicker resource in Jira before version 8.4.0 allows remote attackers to enumerate usernames via an information disclosure vulnerability.  |  2.1 - 8.3.4  |  [CVE-2019-8449](https://lmgtfy.com/?q=CVE-2019-8449)  |
|  CVE-2019-11581  |  CRITICAL  |  Atlassian JIRA Template injection vulnerability RCE  |  Jira < 7.6.14  |  [CVE-2019-11581](https://lmgtfy.com/?q=CVE-2019-11581)  |
|  CVE-2019-8451  |  HIGH  |  Pre-authentication server side request forgery (SSRF) vulnerability found in the /plugins/servlet/gadgets/makeRequest resource.  |  Jira == 7.6.0  && Jira.7.6.0 < 7.13.9, 8.4.0  |  [CVE-2019-8451](https://lmgtfy.com/?q=CVE-2019-8451)  |

Majority of the bugs stated above poses Server-Side Request Forgery (SSRF) vulnerability, where attacker can abuse a specific functionality on the server to read or update internal resources. The attacker can supply or a modify a URL which the code running on the server will read or submit data to, and by carefully selecting the URLs, the attacker may be able to read server configuration such as AWS metadata, connect to internal services like HTTP enabled databases or perform post requests towards internal services which are not intended to be exposed.

Currently, some of the common Amazon AWS credentials leak attacks are present with an additional **Custom Payload Option** for sending crafted payloads for any cloud platform (Amazon AWS, Google Cloud, etc.). For sending custom payloads, take help from [PayloadsAllTheThings &mdash; SSRF URL for Cloud Instances](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery#ssrf-url-for-cloud-instances). Feel free to implement more post exploitation modules for vendor specifc deployments. For looking under the hood, read [wiki](https://github.com/0x48piraj/Jiraffe/wiki/Internals).


## Demonstration

<p align="center">
<img alt="Jiraffe Demo" src="https://raw.githubusercontent.com/0x48piraj/Jiraffe/master/assets/demo.gif">
</p>


## Tests

The tests are next to the package i.e. tests are not part of the package, only of the repository. The reason is simply to keep the package small.

**Running the unit tests**

```shell
$ python3 -m unittest --verbose # Python 3 and up
```


## DISCLAMER

This project is a [personal development](https://en.wikipedia.org/wiki/Personal_development). Please respect it's philosophy and don't use it for evil purposes. By using Jiraffe, you agree to the MIT license included in the repository. For more details at [The MIT License &mdash; OpenSource](https://opensource.org/licenses/MIT).

Using Jiraffe for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.


## Licensing

This project is licensed under the MIT license.