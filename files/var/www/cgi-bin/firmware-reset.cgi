#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Стирание оверлея" %>
<%in p/header.cgi %>
<pre class="bg-light p-4 log-scroll">
<% sysupgrade -n %>
</pre>
<a class="btn btn-primary" href="/">На главную</a>
<a class="btn btn-danger" href="reboot.cgi">Перезагрузить камеру</a>
<%in p/footer.cgi %>
