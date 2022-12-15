#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="mqtt"
plugin_name="MQTT клиент"
page_title="MQTT клиент"
params="enabled host port client_id username password topic message send_snap snap_topic use_ssl"

[ ! -f /usr/bin/mosquitto_pub ] && redirect_to "/" "danger" "MQTT клиент не является частью вашей прошивки."

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
  if [ "true" = "$mqtt_enabled" ]; then
    [ -z "$mqtt_host"      ] && flash_append "danger" "Хост MQTT брокера не может быть пустым." && error=11
    [ -z "$mqtt_port"      ] && flash_append "danger" "MQTT порт не может быть пустым." && error=12
#    [ -z "$mqtt_username"  ] && flash_append "danger" "MQTT логин не может быть пустым." && error=13
#    [ -z "$mqtt_password"  ] && flash_append "danger" "MQTT пароль не может быть пустым." && error=14
    [ -z "$mqtt_topic"     ] && flash_append "danger" "MQTT топик (канал) не может быть пустым." && error=15
    [ -z "$mqtt_message"   ] && flash_append "danger" "MQTT сообщение не может быть пустым." && error=16
  fi

  if [ "${mqtt_topic:0:1}" = "/" ] || [ "${mqtt_snap_topic:0:1}" = "/" ]; then
    flash_append "danger" "MQTT топик (канал) на должен начинаться со слэша." && error=17
  fi

  if [ "$mqtt_topic" != "${mqtt_topic// /}" ] || [ "$mqtt_snap_topic" != "${mqtt_snap_topic// /}" ]; then
    flash_append "danger" "MQTT топик (канал) не должен содержать пробелы." && error=18
  fi

  if [ -n "$(echo $mqtt_topic | sed -r -n /[^\x00-\xFF/]/p)" ] || [ -n "$(echo $mqtt_snap_topic | sed -r -n /[^\x00-\xFF/]/p)" ]; then
    flash_append "danger" "MQTT топик (канал) не должен включать не ASCII символы." && error=19
  fi

  if [ "true" = "$mqtt_send_snap" ] && [ -z "$mqtt_snap_topic" ]; then
    flash_append "danger" "MQTT топик (канал) для снимка не должен быть пустым." && error=20
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

  # Default values
  [ -z "$mqtt_client_id" ] && mqtt_client_id="${network_macaddr//:/}"
  [ -z "$mqtt_port"      ] && mqtt_port="1883"
  [ -z "$mqtt_topic"     ] && mqtt_topic="openipc/${mqtt_client_id}"
  [ -z "$mqtt_message"   ] && mqtt_message=""
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "mqtt_enabled" "Включить MQTT клиент" %>
      <% field_text "mqtt_host" "Хост MQTT брокера" %>
      <% field_switch "mqtt_use_ssl" "Использовать SSL" %>
      <% field_text "mqtt_port" "Порт MQTT брокера" %>
      <% field_text "mqtt_client_id" "ID MQTT клиента" %>
      <% field_text "mqtt_username" "Логин MQTT брокера" %>
      <% field_password "mqtt_password" "Пароль MQTT брокера" %>
      <% field_text "mqtt_topic" "MQTT топик (канал)" %>
      <% field_text "mqtt_message" "MQTT сообщение" "Поддерживает формат <a href=\"https://man7.org/linux/man-pages/man3/strftime.3.html \" target=\"_blank\">strftime()</a>." %>
      <% field_switch "mqtt_send_snap" "Отправить снимок" %>
      <% field_text "mqtt_snap_topic" "MQTT топик (канал) для отправки снимка" %>
      <% field_switch "mqtt_socks5_enabled" "Использовать SOCKS5" "<a href=\"network-socks5.cgi\">НАстроить</a> SOCKS5 доступ" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Скачать лог-файл" "dl.cgi" %>
  </div>
</div>

<script>
$('#mqtt_use_ssl').addEventListener('change', evt => {
  const elPort=$('#mqtt_port');
  if (evt.target.checked) {
    if (elPort.value === "1883") elPort.value="8883";
  } else {
    if (elPort.value === "8883") elPort.value="1883";
  }
});
</script>

<%in p/footer.cgi %>
