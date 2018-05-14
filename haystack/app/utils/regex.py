# -*- coding:utf-8 -*-

"""
Regular expression for parsing url
group[0]
group[1]: scheme
group[2]: "www."
group[3]: host
group[4]: port number
group[5]: path
group[6]: query
"""
url_regex = r'''(?x)\A
([a-z][a-z0-9+\-.]*)://
(www\.)?
([a-z0-9\-._~%]+
|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])
(:[0-9]+)?
([a-zA-Z0-9\-\/._~%!$&'()*+]+)?
(\?[a-zA-Z0-9&=]+)?
'''
