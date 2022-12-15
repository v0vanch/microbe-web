#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Диагностические сообщения" %>
<%in p/header.cgi %>
<% ex "/bin/dmesg" %>
<% button_refresh %>
<% button_download "dmesg" %>
<%in p/footer.cgi %>
