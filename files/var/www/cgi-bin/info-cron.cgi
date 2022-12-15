#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Настройки Cron" %>
<%in p/header.cgi %>
<% ex "cat /etc/crontabs/root" %>
<a class="btn btn-warning" href="texteditor.cgi?f=/etc/crontabs/root">Редактировать файл</a>
<%in p/footer.cgi %>
