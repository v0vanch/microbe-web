#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Статистика сети" %>
<%in p/header.cgi %>
<% ex "netstat -a" %>
<% button_refresh %>
<% button_download "netstat" %>
<%in p/footer.cgi %>
