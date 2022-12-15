#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="tz"
page_title="Временная зона"

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  tmp_file=/tmp/${plugin}.conf
  :>$tmp_file
  [ -z "$POST_tz_name" ] && redirect_to $SCRIPT_NAME "warning" "Пустое наименование временной зоны. Пропуск."
  [ -z "$POST_tz_data" ] && redirect_to $SCRIPT_NAME "warning" "Пустое значение временной зоны. Пропуск."
  [ "$tz_data" != "$POST_tz_data" ] && echo "${POST_tz_data}" >/etc/TZ
  [ "$tz_name" != "$POST_tz_name" ] && echo "${POST_tz_name}" >/etc/timezone
  update_caminfo
  redirect_to $SCRIPT_NAME "success" "Врменная зона обновлена."
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <p><a href="#" id="frombrowser">Определить временную зону по времени браузера</a></p>
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <datalist id="tz_list"></datalist>
      <p class="string">
        <label for="tz_name" class="form-label">Наименование зоны</label>
        <input type="text" id="tz_name" name="tz_name" value="<%= $tz_name %>" class="form-control" list="tz_list">
        <span class="hint text-secondary">Начните вводить название ближайшего крупного города в полу сверху, чтобы выбрать из доступных вариантов.</span>
      </p>
      <p class="string">
        <label for="tz_data" class="form-label">Код зоны</label>
        <input type="text" id="tz_data" name="tz_data" value="<%= $tz_data %>" class="form-control" readonly>
        <span class="hint text-secondary">Код выбранной зоны. Поле только для чтения.</span>
      </p>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat /etc/timezone" %>
    <% ex "cat /etc/TZ" %>
    <% ex "echo \$TZ" %>
  </div>
</div>

<script src="/a/tz.js"></script>
<%in p/footer.cgi %>
