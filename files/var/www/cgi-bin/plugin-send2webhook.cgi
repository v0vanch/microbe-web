#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="webhook"
plugin_name="Отправка на Webhook"
page_title="Отправка на Webhook"
params="enabled url socks5_enabled"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Validation
  if [ "true" = "$webhook_enabled" ]; then
    [ -z "$webhook_url"   ] && flash_append "danger" "URL веб-хука не может быть пустым." && error=11
  fi

  if [ -z "$error" ]; then
    # create temp config file
    :>$tmp_file
    for _p in $params; do
      echo "${plugin}_${_p}=\"$(eval echo \$${plugin}_${_p})\"" >>$tmp_file
    done; unset _p
    mv $tmp_file $config_file

    update_caminfo
    redirect_back "success" "${plugin_name} конфигурация обновлена."
  fi

  redirect_to $SCRIPT_NAME
else
  include $config_file
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "webhook_enabled" "Включить отправку на веб-хук" %>
      <% field_text "webhook_url" "URL веб-хука" %>
      <% field_switch "webhook_socks5_enabled" "Использовать SOCKS5" "<a href=\"network-socks5.cgi\">Настроить</a> SOCKS5 доступ" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Скачать лог-файл" "dl.cgi" %>
  </div>
</div>

<%in p/footer.cgi %>
