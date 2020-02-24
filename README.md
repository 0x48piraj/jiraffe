# Jiraffe

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/makes-people-smile.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/powered-by-responsibility.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/winter-is-coming.svg)](http://forthebadge.com)

<p align="center">
<b>Jiraffe - One stop place for exploiting all Jira instances in your proximity</b><br><br>
<img alt="Jiraffe logo" src="https://raw.githubusercontent.com/0x48piraj/Jiraffe/master/static/logo.png" width="400"><br>
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
|  CVE-2019-11581  |  CRITICAL  |  Atlassian JIRA Template injection vulnerability RCE  |  Jira < 7.6.14  |  [CVE-2019-11581](https://lmgtfy.com/?q=CVE-2019-11581)  |
|  CVE-2019-8451  |  HIGH  |  Pre-authentication server side request forgery (SSRF) vulnerability found in the /plugins/servlet/gadgets/makeRequest resource.  |  Jira == 7.6.0  && Jira.7.6.0 < 7.13.9, 8.4.0  |  [CVE-2019-8451](https://lmgtfy.com/?q=CVE-2019-8451)  |

Majority of the bugs stated above poses Server-Side Request Forgery (SSRF) vulnerability, where attacker can abuse a specific functionality on the server to read or update internal resources. The attacker can supply or a modify a URL which the code running on the server will read or submit data to, and by carefully selecting the URLs, the attacker may be able to read server configuration such as AWS metadata, connect to internal services like HTTP enabled databases or perform post requests towards internal services which are not intended to be exposed.

Currently, some of the common Amazon AWS credentials leak attacks are present with an additional **Custom Payload Option** for sending crafted payloads for any cloud platform (Amazon AWS, Google Cloud, etc.). For sending custom payloads, take help from [PayloadsAllTheThings &mdash; SSRF URL for Cloud Instances](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery#ssrf-url-for-cloud-instances)

##### URL Paths Jiraffe Currently Supports:
```
Root Path: /latest/meta-data/{hostname,public-ipv4,...}
User Data : /latest/user-data
AWS Credentials : /latest/meta-data/iam/security-credentials/
```

Feel free to implement more post exploitation modules for vendor specifc deployments.

## Demo

![Jiraffe Demo](https://raw.githubusercontent.com/0x48piraj/Jiraffe/master/static/demo.gif)

## Internal Workings

#### Reconnaissance &mdash; Jira version detection

If unauthenticated, one can access Confluence's landing page and retrieve version information from these places:

- Login page footer.

![](https://confluence.atlassian.com/confkb/files/980460833/980460769/1/1574450271730/Screen+Shot+2019-11-22+at+14.25.48.png)

- Response Head AJS Tags.

![](https://confluence.atlassian.com/confkb/files/980460833/980460798/1/1574450271658/Screen+Shot+2019-11-22+at+15.07.51.png)

- Response Body What's New Link.

![](https://confluence.atlassian.com/confkb/files/980460833/980460799/1/1574450271373/Screen+Shot+2019-11-22+at+15.10.01.png)

- Response Body Confluence Help Link.

![](https://confluence.atlassian.com/confkb/files/980460833/982321522/1/1576094162892/Screen+Shot+2019-12-11+at+16.55.54.png)


## References

- [RCE in Jira (CVE-2019–11581)](https://medium.com/@ruvlol/rce-in-jira-cve-2019-11581-901b845f0f)
- [One Misconfig (JIRA) to Leak Them All- Including NASA and Hundreds of Fortune 500 Companies!](https://medium.com/@logicbomb_1/one-misconfig-jira-to-leak-them-all-including-nasa-and-hundreds-of-fortune-500-companies-a70957ef03c7)