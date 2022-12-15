#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Логи" %>
<%in p/header.cgi %>
<% ex "/sbin/logread" %>
<% button_refresh %>
<% button_download "logread" %>

<% if [ -z "$(eval echo "DEBUG TRACE" | sed -n "/\b$(yaml-cli -g .system.logLevel)\b/p")" ]; then %>
<div class="alert alert-warning my-3">
<p><a class="btn btn-warning disabled">Загрузить логи Majectic на PasteBin</a></p>
<p class="mb-0">Пожалуйста, включите DEBUG level для логгирования <a href="majestic-settings.cgi?tab=system">в конфигурации Majectic</a>, чтобы активировать эту функцию.</p>
</div>
<% else %>
<a class="btn btn-warning" href="send.cgi?to=pastebin&file=mjlog" target="_blank">Загрузить логи Majectic на PasteBin</a>
<% fi %>

<%in p/footer.cgi %>
