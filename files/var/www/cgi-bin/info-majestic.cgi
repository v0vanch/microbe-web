#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Конфигурация Majestic" %>
<%in p/header.cgi %>
<% ex "cat /etc/majestic.yaml" %>
<a class="btn btn-warning" href="texteditor.cgi?f=/etc/majestic.yaml">Редактировать файл</a>
<%in p/footer.cgi %>
