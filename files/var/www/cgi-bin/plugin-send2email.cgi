#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="email"
plugin_name="Отправка по Email"
page_title="Отправка по Email"
params="enabled attach_snapshot from_name from_address to_name to_address subject body smtp_host smtp_port smtp_username smtp_password smtp_use_ssl socks5_enabled"

tmp_file=/tmp/${plugin}.conf

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
  # parse values from parameters
  for _p in $params; do
    eval ${plugin}_${_p}=\$POST_${plugin}_${_p}
    sanitize "${plugin}_${_p}"
  done; unset _p

  ### Normalization
  email_body="$(echo "$email_body" | tr "\r?\n" " ")"

  ### Validation
  if [ "true" = "$email_enabled" ]; then
    [ -z "$email_smtp_host"    ] && flash_append "danger" "SMTP хост не может быть пустым." && error=11
    [ -z "$email_from_address" ] && flash_append "danger" "Email адрес отправителя не может быть пустым." && error=12
    [ -z "$email_from_name"    ] && flash_append "danger" "Имя отправителя не может быть пустым." && error=13
    [ -z "$email_to_address"   ] && flash_append "danger" "Email адрес получателя не может быть пустым." && error=14
    [ -z "$email_to_name"      ] && flash_append "danger" "Имя получателя не может быть пустым." && error=15
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
  [ -z "$email_attach_snapshot" ] && email_attach_snapshot="true"
  [ -z "$email_smtp_port" ] && email_smtp_port="25"
  [ -z "$email_from_name" ] && email_from_name="Камера ${network_hostname}"
  [ -z "$email_to_name" ] && email_to_name="Администратор камеры"
#  [ -z "$email_subject" ] && email_subject="Снимок с камеры ${network_hostname}"
fi
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <form action="<%= $SCRIPT_NAME %>" method="post">
      <% field_switch "email_enabled" "Включить отправку по Email" %>
      <% field_text "email_smtp_host" "SMTP хост" %>
      <% field_text "email_smtp_port" "SMTP порт" %>
      <% field_switch "email_smtp_use_ssl" "Использовать TLS/SSL" %>
      <% field_text "email_smtp_username" "SMTP логин" %>
      <% field_password "email_smtp_password" "SMTP пароль" %>
      <% field_text "email_from_name" "Имя отправителя" %>
      <% field_text "email_from_address" "Адрес отправителя" "Use an email address where bounce reports can be sent to." %>
      <% field_text "email_to_name" "Имя получателя" %>
      <% field_text "email_to_address" "Адрес получателя" %>
      <% field_text "email_subject" "Тема письма" %>
      <% field_textarea "email_body" "Текст письма" "Переносы строки будут заменены пробелами." %>
      <% field_switch "email_attach_snapshot" "Прикрепить снимок" %>
      <% # field_switch "email_socks5_enabled" "Использовать SOCKS5" "<a href=\"network-socks5.cgi\">Настроить</a> SOCKS5 доступ" %>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <% ex "cat $config_file" %>
    <% [ -f "/tmp/webui.log" ] && link_to "Скачать лог-файл" "dl.cgi" %>
  </div>
</div>

<script>
$('#email_body').style.height = "6rem";

$('#email_smtp_use_ssl').addEventListener('change', evt => {
  const elPort=$('#email_smtp_port');
  if (evt.target.checked) {
    if (elPort.value === "25") elPort.value="465";
  } else {
    if (elPort.value === "465") elPort.value="25";
  }
});
</script>

<%in p/footer.cgi %>
