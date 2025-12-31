#!/usr/bin/env python3
# -*- coding: utf-8 -*-

AWS_INSTANCE = "http://169.254.169.254/latest"
AWS_METADATA = "http://169.254.169.254/latest/meta-data/"
AWS_IAM_DATA = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
AWS_IAM_CRED = AWS_IAM_DATA + "%s" #<rolename>
DEFAULT_SSRF_TEST = "https://www.google.com"
