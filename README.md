# Jiraffe

<p align="center">
<b>Jiraffe - One stop place for exploiting all Jira instances in your proximity</b><br><br>
<img alt="Jiraffe logo" src="static/logo.png" width="400"><br>
See the <a href="#demo">demo</a>
</p>

## Installation

Use pip to install **Jiraffe**. This is the recommended way of running Jiraffe.

```
$ pip install jiraffe
```

#### Usage

```
$ py -m jiraffe
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

## Exploits for

|  CVE  |  Impact  |  Description  |  Version Affected  |  Details  |
|---|---|---|---|---|
|  CVE-2017-9506  |  HIGH  |  The IconUriServlet of the Atlassian OAuth Plugin from version 1.3.0 before version 1.9.12 and from version 2.0.0 before version 2.0.4 allows remote attackers to access the content of internal network resources and/or perform an XSS attack via Server Side Request Forgery (SSRF).  |  Jira < 7.3.5  |  [CVE-2017-9506](https://lmgtfy.com/?q=CVE-2017-9506)  |
|  CVE-2019-8449  |  LOW  |  The /rest/api/latest/groupuserpicker resource in Jira before version 8.4.0 allows remote attackers to enumerate usernames via an information disclosure vulnerability.  |  2.1 - 8.3.4  |  [CVE-2019-8449](https://lmgtfy.com/?q=CVE-2019-8449)  |
|  CVE-2019-11581  |  VERY HIGH  |  Atlassian JIRA Template injection vulnerability RCE  |  Jira < 7.6.14  |  [CVE-2019-11581](https://lmgtfy.com/?q=CVE-2019-11581)  |
|  CVE-2019-8451  |  HIGH  |  Pre-authentication server side request forgery (SSRF) vulnerability found in the /plugins/servlet/gadgets/makeRequest resource.  |  Jira == 7.6.0  && Jira.7.6.0 < 7.13.9, 8.4.0  |  [CVE-2019-8451](https://lmgtfy.com/?q=CVE-2019-8451)  |

Majority of the bugs stated above poses Server-Side Request Forgery (SSRF) vulnerability, where attacker can abuse a specific functionality on the server to read or update internal resources. The attacker can supply or a modify a URL which the code running on the server will read or submit data to, and by carefully selecting the URLs, the attacker may be able to read server configuration such as AWS metadata, connect to internal services like HTTP enabled databases or perform post requests towards internal services which are not intended to be exposed.

For further exploitation, I'll most likely write some post exploitation scripts for vendor specifc deployments.

## Reconnaissance

#### Jira version detection

If unauthenticated, one can access Confluence's landing page and retrieve version information from these places:

- Login page footer.

![](https://confluence.atlassian.com/confkb/files/980460833/980460769/1/1574450271730/Screen+Shot+2019-11-22+at+14.25.48.png)

- Response Head AJS Tags.

![](https://confluence.atlassian.com/confkb/files/980460833/980460798/1/1574450271658/Screen+Shot+2019-11-22+at+15.07.51.png)

- Response Body What's New Link.

![](https://confluence.atlassian.com/confkb/files/980460833/980460799/1/1574450271373/Screen+Shot+2019-11-22+at+15.10.01.png)

- Response Body Confluence Help Link.

![](https://confluence.atlassian.com/confkb/files/980460833/982321522/1/1576094162892/Screen+Shot+2019-12-11+at+16.55.54.png)