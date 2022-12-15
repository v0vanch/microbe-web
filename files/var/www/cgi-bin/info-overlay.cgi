#!/usr/bin/haserl
<%in p/common.cgi %>
<%
_s=$(df | grep /overlay | xargs | cut -d' ' -f5)
page_title="Содержимое раздела оверлея"
%>
<%in p/header.cgi %>
<div class="alert alert-primary">
  <h5>Раздел оверлея заполнен на <%= $_s %>.</h5>
  <% progressbar "${_s/%/}" %>
</div>
<% ex "ls -Rl /overlay/" %>
<%in p/reset-firmware.cgi %>
<%in p/footer.cgi %>
